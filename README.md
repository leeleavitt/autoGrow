# autoGrow
This is a software used to control various parts of an automatic grow system i am developing for growing all plants from seed this year.

I built a wooden frame from 2 by 4's. This was required since we are going to place a 5 gallon bucket on the top of this system to control the watering of the seedlings. Additionally, to prevent slipping I cut custom rubber pads from rubber gasket found in the plumbing section and stapled this to the bottom of the stand to prevent slippage. 

We have many parts to control.

1. Controling the [Kingled 1000w](https://www.amazon.com/Double-Spectrum-Greenhouse-Indoor-Flower/dp/B0185OLBPK). Here we used an simple to use [Iot relay](https://www.amazon.com/gp/product/B00WV7GMA2/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1) since we are working with a high powered light.

   I decided to control the light using the `BCM pin 17`

2. Here we have [2 VIVOSUN fans](https://www.amazon.com/gp/product/B07QW4YK9S/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1). These fans attach with a clamp to a tent pole, so to get them to attach to my wooden frame I added a pipe manifold for the fans to connect to. 

3. Gravity irrigation is controlled by a [12 volt 1/4" solenoid valve](https://www.amazon.com/gp/product/B00APDNPXG/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1). Since this part has a 12V and 12W rating, controlling this required purchasing a [12V 1A power supply](https://www.amazon.com/gp/product/B07QLKQLQQ/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1). 

4. To control **1 and 2** above, I am using the [ELEGOO 8 channel DC 5V Relay Module](https://www.amazon.com/gp/product/B01HCFJC0Y/ref=ppx_yo_dt_b_asin_title_o05_s01?ie=UTF8&psc=1). I decided to follow Techplants [instructions](https://www.youtube.com/watch?v=Ur0w7VeLX08). Since this project has potential to add more solenoid valves, I decided to go with the 8 channel relay
   
   This relay requires outside power. So I am using a [5V 1A](https://www.amazon.com/gp/product/B07KVZHVCS/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1) power supply.

5. Finished making the reflective material for the grow house using this [vivosun reflective mylar](https://www.amazon.com/gp/product/B018VI75CS/ref=ppx_yo_dt_b_asin_title_o05_s02?ie=UTF8&th=1). This prevents most of the light from escaping the room. Made frames from wood and butt joints

6. Added a [Craftsman LED](https://www.lowes.com/pd/CRAFTSMAN-2000-Lumen-LED-Portable-Work-Light/1000598689) yellow light. I turn this light on and the grow light off to take an image for the timelapse imaging.

Current pins in use

Added a new feature to control the fans at specified intervals. Within the `SETTINGS.json` file i have added `fanTime`, this is a list of lists. For example to have the fan turn for specified times during the day add a new list item to it 
```
"fanTime":[[10,12],[20,22]]
```
This means the fan will run between 10am and noon, and then from 8p to 10p


**17: Light**

**6: Fan Left side**

**13: Fan Right side**

**5: Solenoid Valve**

**26: Craftsman LED Yellow Light**


I've added a cron job, where after typing `crontab -e` i added the following line of code to the document.

```*/30 *    * * *   sudo python3 /home/pi/Documents/autoGrow/py/autoGrow.py > /dev/null 2>&1```