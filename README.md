# SunFounder Pico-4wd Car Kit V2
This is the code, drivers and some documents for Pico-4wd Car.You can buy it on [our website](https://www.sunfounder.com/), or search sunfounder in Amazon.

- [Pico-4wd Car](#nano-sloth-kit)
- [Related Links](#related-links)
- [File Tree](#file-tree)
- [About SunFounder](#about-sunfounder)
- [Contact Us](#contact-us)

## Pico-4wd Car
<div align="center">
    <img src="./img/PICO-4WD-V2.png" width="80%" height="80%"   align="center" title="PICO-4WD-V2"/>
    &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
    <!-- <img src="./img/Nano_Sloth_V2.png" width="212" height="261" align="center" title="Nano_Sloth_V2"/> -->
</div>

The Pico-4wd is a Raspberry Pi Pico based, cool, robot car kit that everyone can have.

Equipped with greyscale sensor module and ultrasonic module, it can perform line tracking, cliff detection, follow and obstacle avoidance functions. The RGB boards assembled at the bottom and rear of the car make it the coolest spirit in the dark.

We have provided sample code based on MicroPython so you can get started quickly.

In addition, you can also use an app - SunFounder Controller - to DIY your own control methods!

## Related Links
- documentation:
    https://docs.sunfounder.com/projects/pico-4wd-car/en/latest/index.html
- our website:
    https://sunfounder.com

## File Tree

    pico_4wd_car                               
    ├─ esp8266-uart-wsserver   // websocket-uart firmware for esp01s                
    ├─ examples                // examples                
    │  ├─ app_control.py                       
    │  ├─ app_control_v2.py                    
    │  ├─ battery_test.py                      
    │  ├─ bull_fight.py                        
    │  ├─ donot_push_me.py                     
    │  ├─ follow_hand.py                       
    │  ├─ follow_hand_v2.py                    
    │  ├─ line_track.py                        
    │  ├─ mileage_test.py                      
    │  └─ obstacle_avoid.py                    
    ├─ img                                     
    ├─ libs                    // library                
    │  ├─ pico_4wd.py                          
    │  ├─ pico_rdp.py                          
    │  └─ ws.py                                
    ├─ tests                   // test examples                
    │  ├─ app_test.py                          
    │  ├─ light_effect.py                      
    │  ├─ pico_4wd_test.py                     
    │  ├─ test.py                              
    │  ├─ test_grayscale.py                    
    │  ├─ test_light.py                        
    │  ├─ test_motor.py                        
    │  ├─ test_servo.py                        
    │  ├─ test_sonar.py                        
    │  └─ test_speed.py                        
    ├─ api_reference_pico_4wd.md               
    └─ README.md                               


## About SunFounder
SunFounder is a company focused on STEAM education with products like open source robots, development boards, STEAM kit, modules, tools and other smart devices distributed globally. In SunFounder, we strive to help elementary and middle school students as well as hobbyists, through STEAM education, strengthen their hands-on practices and problem-solving abilities. In this way, we hope to disseminate knowledge and provide skill training in a full-of-joy way, thus fostering your interest in programming and making, and exposing you to a fascinating world of science and engineering. To embrace the future of artificial intelligence, it is urgent and meaningful to learn abundant STEAM knowledge.

## Contact Us
website:
    <a href="https://www.sunfounder.com" target="_blank">www.sunfounder.com</a>

E-mail:
    service@sunfounder.com