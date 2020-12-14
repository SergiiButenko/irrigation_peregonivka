
#ifndef STASSID
#define STASSID "faza_2"
#define STAPSK "Kobe_2016"
//#define STASSID "Notebooks"
//#define STAPSK "0660101327"
#endif

const char* flash_version = "23-00.apr-07-2020";
const char* device_id = "8chrelay_1";
const char* ssid = STASSID;
const char* password = STAPSK;

// relay num starts from 1. so add 1 to skip 0;
const byte num_of_relay = 8 + 1;
// relay id is index, pin number is value 
//                             0  1  2  3  4   5   6   7   8
int relay_pins[num_of_relay]={-1, 5, 4, 0, 2, 14, 12, 13, 15};



// relay num starts from 1. so add 1 to skip 0;
//const byte num_of_relay = 2 + 1;
// relay id is index, pin number is value 
//                             0  1  2
//int relay_pins[num_of_relay]={-1, 5, 4};
