What about
for i in $(cat urlList.txt) do ; dig +short $i ; done 



This script takes a list of URLs and generates the appropriate ACL
the ACL is used on wag1.mel8 to not account for ISG traffic when users on VicFreeWiFi
go to one of these websites.

The URL list was gleened orginally from Content Keeper by Content Keeper


Below is the ISG config for reference only June 2018

aaa group server radius VicFreeWiFi-Quota-Mgmt
 server name per-qv1-wifiradius1
 ip radius source-interface GigabitEthernet0/0/5.211
!
aaa accounting network VicFreeWiFi-Accounting
 action-type start-stop periodic interval 5
 group VicFreeWiFi-Quota-Mgmt
!
class-map type traffic match-any VIC-GOV-UNMETER-CLASS
 match access-group output name VIC-GOV-UNMETER-LIST
!
policy-map type service IDLE-TIMER
  keepalive idle 300 attempts 3 interval 5 protocol ARP
!
policy-map type service VIC-FREE-ACCOUNTING
 class type traffic VIC-GOV-UNMETER-CLASS
  accounting aaa list VicFreeWiFi-Accounting
 !
!
policy-map type control Vlan103
 class type control always event session-start
  10 service-policy type service name VIC-FREE-ACCOUNTING
  20 service-policy type service name IDLE-TIMER
  30 authorize identifier mac-address 
 !

interface TenGigabitEthernet0/2/0.103
 description --- Vlan103 SSID's (CK+VicISG) ---
 encapsulation dot1Q 103
 ip address 100.79.0.1 255.255.0.0
 no ip proxy-arp
 ip nat inside
 ip verify unicast reverse-path
 ip access-group 101 in
 arp timeout 900
 service-policy type control Vlan103
 ip subscriber l2-connected
  initiator unclassified mac-address

