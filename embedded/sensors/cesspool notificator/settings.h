
#ifndef STASSID
#define STASSID "faza_2"
#define STAPSK "Kobe_2016"
//#define STASSID "Notebooks"
//#define STAPSK "0660101327"
#endif

const char* flash_version = "00-00.jan-31-2021";
const char* device_id = "cesspool_relay1";
const char* ssid = STASSID;
const char* password = STAPSK;

// relay num starts from 1. so add 1 to skip 0;
// const byte num_of_relay = 8 + 1;
// const byte num_of_relay = 4 + 1;
const byte num_of_relay = 2 + 1;

// relay id is index, pin number is value 
//                             0  1  2  3  4   5   6   7   8
// int relay_pins[num_of_relay]={-1, 5, 4, 0, 2, 14, 12, 13, 15};
int relay_pins[num_of_relay]={-1, 5, 4};
// int relay_pins[num_of_relay]={4, 5, 12, 13};


const char *host = "http://mozz.breeze.ua:9000";
byte delay_between_requests = 500;
byte delay_for_counter_millis = 10;
byte retry_limit = 3;
const long registration_interval = 1000 * 30;
