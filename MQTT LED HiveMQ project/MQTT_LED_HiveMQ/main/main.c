#include <stdio.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "esp_log.h"
#include "esp_event.h"
#include "esp_netif.h"
#include "esp_wifi.h"
#include "nvs_flash.h"

#include "driver/gpio.h"

#include "mqtt_client.h"
#include "esp_crt_bundle.h"


/* =========================================================
 * CONFIGURATION
 * =========================================================
 */

/* External LED is connected to GPIO 4 */
#define LED_GPIO GPIO_NUM_4

/* Wi-Fi credentials */
#define WIFI_SSID "HOTSPOT NAME"
#define WIFI_PASSWORD "PASSWORD"

/* HiveMQ Cloud */
#define MQTT_BROKER_URI "mqtts://9acc69a4fa1646a0878d3072c1407b30.s1.eu.hivemq.cloud:8883"

#define MQTT_USERNAME "Username"
#define MQTT_PASSWORD "Password"

/* MQTT topic */
#define MQTT_TOPIC "esp32/led"


static const char *TAG = "MQTT_LED";


/* =========================================================
 * LED INITIALIZATION
 * =========================================================
 */

static void led_init(void)
{
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << LED_GPIO),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE
    };

    ESP_ERROR_CHECK(gpio_config(&io_conf));

    /* Start with LED OFF */
    gpio_set_level(LED_GPIO, 0);
}


/* =========================================================
 * WIFI EVENT HANDLER
 * =========================================================
 */

static void wifi_event_handler(
    void *arg,
    esp_event_base_t event_base,
    int32_t event_id,
    void *event_data)
{
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START)
    {
        ESP_LOGI(TAG, "Wi-Fi started");
        esp_wifi_connect();
    }

    else if (event_base == WIFI_EVENT &&
             event_id == WIFI_EVENT_STA_DISCONNECTED)
    {
        ESP_LOGW(TAG, "Wi-Fi disconnected. Reconnecting...");
        esp_wifi_connect();
    }

    else if (event_base == IP_EVENT &&
             event_id == IP_EVENT_STA_GOT_IP)
    {
        ip_event_got_ip_t *event = (ip_event_got_ip_t *)event_data;

        ESP_LOGI(
            TAG,
            "Got IP: " IPSTR,
            IP2STR(&event->ip_info.ip)
        );
    }
}


/* =========================================================
 * WIFI INITIALIZATION
 * =========================================================
 */

static void wifi_init(void)
{
    ESP_ERROR_CHECK(esp_netif_init());

    ESP_ERROR_CHECK(
        esp_event_loop_create_default()
    );

    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();

    ESP_ERROR_CHECK(
        esp_wifi_init(&cfg)
    );

    ESP_ERROR_CHECK(
        esp_event_handler_register(
            WIFI_EVENT,
            ESP_EVENT_ANY_ID,
            &wifi_event_handler,
            NULL
        )
    );

    ESP_ERROR_CHECK(
        esp_event_handler_register(
            IP_EVENT,
            IP_EVENT_STA_GOT_IP,
            &wifi_event_handler,
            NULL
        )
    );

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASSWORD,
        },
    };

    ESP_ERROR_CHECK(
        esp_wifi_set_mode(WIFI_MODE_STA)
    );

    ESP_ERROR_CHECK(
        esp_wifi_set_config(
            WIFI_IF_STA,
            &wifi_config
        )
    );

    ESP_ERROR_CHECK(
        esp_wifi_start()
    );

    ESP_LOGI(TAG, "Connecting to Wi-Fi...");
}


/* =========================================================
 * MQTT EVENT HANDLER
 * =========================================================
 */

static void mqtt_event_handler(
    void *handler_args,
    esp_event_base_t base,
    int32_t event_id,
    void *event_data)
{
    esp_mqtt_event_handle_t event =
        (esp_mqtt_event_handle_t)event_data;

    esp_mqtt_client_handle_t client =
        event->client;

    switch ((esp_mqtt_event_id_t)event_id)
    {
        case MQTT_EVENT_CONNECTED:

            ESP_LOGI(TAG, "MQTT CONNECTED");

            /*
             * Subscribe to:
             *
             * esp32/led
             */
            esp_mqtt_client_subscribe(
                client,
                MQTT_TOPIC,
                1
            );

            ESP_LOGI(
                TAG,
                "Subscribed to topic: %s",
                MQTT_TOPIC
            );

            break;


        case MQTT_EVENT_DISCONNECTED:

            ESP_LOGW(TAG, "MQTT DISCONNECTED");

            break;


        case MQTT_EVENT_SUBSCRIBED:

            ESP_LOGI(
                TAG,
                "MQTT SUBSCRIBED, msg_id=%d",
                event->msg_id
            );

            break;


        case MQTT_EVENT_DATA:

            ESP_LOGI(TAG, "MQTT DATA RECEIVED");

            /*
             * Print received topic
             */
            printf(
                "Topic: %.*s\n",
                event->topic_len,
                event->topic
            );

            /*
             * Print received message
             */
            printf(
                "Data: %.*s\n",
                event->data_len,
                event->data
            );


            /* -----------------------------------------
             * LED CONTROL
             * -----------------------------------------
             */

            if (
                event->data_len == 2 &&
                strncmp(event->data, "ON", 2) == 0
            )
            {
                gpio_set_level(LED_GPIO, 1);

                ESP_LOGI(
                    TAG,
                    "LED -> ON"
                );
            }

            else if (
                event->data_len == 3 &&
                strncmp(event->data, "OFF", 3) == 0
            )
            {
                gpio_set_level(LED_GPIO, 0);

                ESP_LOGI(
                    TAG,
                    "LED -> OFF"
                );
            }

            else
            {
                ESP_LOGW(
                    TAG,
                    "Unknown command. Use ON or OFF"
                );
            }

            break;


        case MQTT_EVENT_ERROR:

            ESP_LOGE(TAG, "MQTT ERROR");

            if (event->error_handle != NULL)
            {
                ESP_LOGE(
                    TAG,
                    "MQTT error type: %d",
                    event->error_handle->error_type
                );

                if (
                    event->error_handle->esp_tls_last_esp_err
                )
                {
                    ESP_LOGE(
                        TAG,
                        "ESP TLS error: 0x%x",
                        event->error_handle
                            ->esp_tls_last_esp_err
                    );
                }

                if (
                    event->error_handle->esp_tls_stack_err
                )
                {
                    ESP_LOGE(
                        TAG,
                        "TLS stack error: 0x%x",
                        event->error_handle
                            ->esp_tls_stack_err
                    );
                }
            }

            break;


        default:

            ESP_LOGI(
                TAG,
                "MQTT event ID: %" PRIi32,
                event_id
            );

            break;
    }
}


/* =========================================================
 * MQTT INITIALIZATION
 * =========================================================
 */

static void mqtt_app_start(void)
{
    ESP_LOGI(
        TAG,
        "Starting MQTT..."
    );


    esp_mqtt_client_config_t mqtt_cfg = {

        /*
         * HiveMQ Cloud MQTT TLS URL
         */
        .broker.address.uri = MQTT_BROKER_URI,


        /*
         * HiveMQ username/password
         */
        .credentials.username = MQTT_USERNAME,

        .credentials.authentication.password =
            MQTT_PASSWORD,


        /*
         * IMPORTANT:
         *
         * Use ESP-IDF's trusted certificate bundle
         * for TLS server verification.
         */
        .broker.verification.crt_bundle_attach =
            esp_crt_bundle_attach,
    };


    esp_mqtt_client_handle_t client =
        esp_mqtt_client_init(&mqtt_cfg);


    if (client == NULL)
    {
        ESP_LOGE(
            TAG,
            "Failed to initialize MQTT client"
        );

        return;
    }


    ESP_ERROR_CHECK(
        esp_mqtt_client_register_event(
            client,
            ESP_EVENT_ANY_ID,
            mqtt_event_handler,
            NULL
        )
    );


    ESP_ERROR_CHECK(
        esp_mqtt_client_start(client)
    );


    ESP_LOGI(
        TAG,
        "MQTT client started"
    );
}


/* =========================================================
 * APP MAIN
 * =========================================================
 */

void app_main(void)
{
    /*
     * Initialize NVS
     */
    esp_err_t ret = nvs_flash_init();

    if (
        ret == ESP_ERR_NVS_NO_FREE_PAGES ||
        ret == ESP_ERR_NVS_NEW_VERSION_FOUND
    )
    {
        ESP_ERROR_CHECK(
            nvs_flash_erase()
        );

        ESP_ERROR_CHECK(
            nvs_flash_init()
        );
    }

    ESP_LOGI(
        TAG,
        "Starting MQTT LED project..."
    );


    /*
     * Initialize external LED
     */
    led_init();


    /*
     * Initialize Wi-Fi
     */
    wifi_init();


    /*
     * Give Wi-Fi some time to connect
     *
     * MQTT will start after Wi-Fi initialization.
     */
    vTaskDelay(
        pdMS_TO_TICKS(5000)
    );


    /*
     * Start MQTT
     */
    mqtt_app_start();


    /*
     * app_main can return.
     * MQTT and Wi-Fi run in their own tasks.
     */
}
