#Metric Converter

print "Format: [value] [measure]."
print "Measures accepted: Length: mm-km and in-mi. Mass: g-mt and"
print "oz-t. Area: cm2-km2 and in2-mi2. Volume: ml-kl/cm3-m3"
print "and floz-ga/in3-yd3. Temperature: f and c.\n"

def lowercase(string):
    out=""
    count=0
    while count<len(string):
        if ord(string[count])>64 and ord(string[count])<91:
            out+=chr(ord(string[count])+32)
        else:
            out+=string[count]
        count+=1
    return out

loop=1
while loop!=0:
    x=raw_input("")
    x=lowercase(x)
    n=1
    space=False
    while space==False:
        if x[n]==" ":
            space=True
        n+=1
    value=float(x[0:n-1])
    measure=x[n:]
    
#metric length to english length
    
    if measure=="mm":
        value*=.039
        measure="in-"
    if measure=="cm":
        value*=.39
        measure="in-"
    if measure=="m":
        value*=39.37
        measure="in-"
    if measure=="km":
        value*=39370.08
        measure="in-"
    if value>=12 and measure=="in-":
        value/=12.0
        measure="ft-"
        if value>=5280:
            value/=5280.0
            measure="mi-"
                
#english length to metric length
                
    if measure=="in":
        value*=25.4
        measure="mm-"
    if measure=="ft":
        value*=304.8
        measure="mm-"
    if measure=="mi":
        value*=1609344
        measure="mm-"
    if value>=10 and measure=="mm-":
        value/=10.0
        measure="cm-"
        if value>=100:
            value/=100.0
            measure="m-"
            if value>=100:
                value/=1000.0
                measure="km-"

#metric mass to english mass
                    
    if measure=="g":
        value*=.035
        measure="oz-"
    if measure=="kg":
        value*=35.27
        measure="oz-"
    if measure=="mt":
        value*=35273.96
        measure="oz-"
    if value>=16 and measure=="oz-":
        value/=16.0
        measure="lb-"
        if value>=2000:
            value/=2000.0
            measure="t-"

#english mass to metric mass
                
    if measure=="oz":
        value*=28.35
        measure="g-"
    if measure=="lb":
        value*=453.59
        measure="g-"
    if measure=="t":
        value*=907184.74
        measure="g-"
    if value>=1000 and measure=="g-":
        value/=1000.0
        measure="kg-"
        if value>=1000:
            value/=1000.0
            measure="mt-"

#metric volume to english volume (liquid)
                
    if measure=="ml":
        value*=.034
        measure="floz-"
    if measure=="l":
        value*=33.81
        measure="floz-"
    if measure=="kl":
        value*=33814.023
        measure="floz-"
    if value>=16 and measure=="floz-":
        value/=16.0
        measure="pt-"
        if value>=2:
            value/=2.0
            measure="qt-"
            if value>=4:
                value/=4.0
                measure="ga-"

#english volume to metric volume (liquid)

    if measure=="floz":
        value*=29.57
        measure="ml-"
    if measure=="pt":
        value*=473.18
        measure="ml-"
    if measure=="qt":
        value*=946.35
        measure="ml-"
    if measure=="ga":
        value*=3785.41
        measure="ml-"
    if value>=1000 and measure=="ml-":
        value/=1000.0
        measure="l-"
        if value>=1000:
            value/=1000.0
            measure="kl-"

#metric voulme to english volume (cubic)
                
    if measure=="cm3":
        value*=.061
        measure="in3-"
    if measure=="m3":
        value*=61023.74
        measure="in3-"
    if value>=1728 and measure=="in3-":
        value/=1728.0
        measure="ft3-"
        if value>=27:
            value/=27.0
            measure="yd3-"

#english volume to metric volume (cubic)

    if measure=="in3":
        value*=16.39
        measure="cm3-"
    if measure=="ft3":  
        value*=28316.85
        measure="cm3-"
    if measure=="yd3":
        value*=764554.86
        measure="cm3-"
    if value>=1000000 and measure=="cm3-":
        value/=1000000.0
        measure="m3-"

#metric area to english area
            
    if measure=="cm2":
        value*=.155
        measure="in2-"
    if measure=="m2":
        value*=1550
        measure="in2-"
    if measure=="km2":
        value*=1550003100
        measure="in2-"
    if value>=144 and measure=="in2-":
        value/=144.0
        measure="ft2-"
        if value>=27878400:
            value/=27878400.0
            measure="mi2-"

#english area to metric area

    if measure=="in2":
        value*=6.45
        measure="cm2-"
    if measure=="ft2":
        value*=929.03
        measure="cm2-"
    if measure=="mi2":
        value*=25899881103.36
        measure="cm2-"
    if value>=10000 and measure=="cm2-":
        value/=10000.0
        measure="m2-"
        if value>=1000000:
            value/=1000000.0
            measure="km2-"
                    
#temperature conversions
                    
    if measure=="f":
        value=(((value-32)*5)/9.0)
        measure="c-"
    if measure=="c":
        value=(((value*9)/5.0)+32)
        measure="f-"

    print str(round(value, 2)) + " " + measure[:len(measure)-1] + "\n"
