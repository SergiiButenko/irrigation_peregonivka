#ifndef STASSID
#define STASSID "faza_2"
#define STAPSK "Kobe_2016"
#endif

const char* flash_version = "00-00.jan-01-2021";
const char* device_id = "cesspool_notificator";
const char* ssid = STASSID;
const char* password = STAPSK;

const char *host = "http://irrigation.faza:9000/api/v1";
byte delay_between_requests = 500;
byte delay_for_counter_millis = 10;
byte retry_limit = 3;
const long interval = 1000 * 60 * 5;
const long registration_interval = 1000 * 30;
