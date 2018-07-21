#!/usr/bin/env python
'''
OVERVIEW:
Test script for sending UDP commands.

AUTHORS:
Bronson Edralin <bedralin@hawaii.edu> & Isar Mostafanezhad
University of Hawaii at Manoa
Instrumentation Development Lab (IDLab), WAT214
DESCRIPTION:
chmod +x tst_sendUDP.py
./tst_sendUDP.py
9/18/2015, IM: Separated each ASIC config sequence and added wait states.
9/21/2015, IM: Updated config values to the latest
'''




import sys
import os
import time
#SCRIPTPATH = os.path.dirname(__file__)
#sys.path.append( SCRIPTPATH+'/lib/' )
sys.path.append( os.getcwd()+'/lib/' )
import linkEth

usageMSG="Usage: setMBTXConfig <interface> \n This command will set the config parameters of all the ASICs on the MB"
if len(sys.argv)!=2:
	print usageMSG
	exit(-1)



# Ethernet Configuration
addr_fpga = '192.168.20.5'
addr_pc = '192.168.20.1'
port_pc = '28672'
port_fpga = '24576'
interface = sys.argv[1]

# Make UDP class for receiving/sending UDP Packets
ctrl = linkEth.UDP(addr_fpga, port_fpga, addr_pc, port_pc, interface)

ctrl.open()
syncwd="000000010253594e4300000000"
#TH="DAC";#3500
#TH="C1C";#3100
#TH="D48";#3400
#TH="D84";#3460
TH="D98";#3480

cmd_pre=""+\
"01234567"+"AE000100"+\
"AF000000"+"AE000100"+\
"AF008000"+"AE000100"+"AE008000"+"AE000100"+"AE000100"+\
"AF00FFFF"+"AE000100"+"AE000100"+\
"AF008000"+"AE000100"+\
"AF050080"+"AE000100"+\
"AF060140"+"AE000100"+\
"AF300004"+"AE000100"+\
"AF2F0004"+"AE000100"
# last two wait cmd's added by CK (was missing---though maybe not necessary here)


######################## TargetX Register Format ###############################
##
##      "D98": even registers 0-14 (Trig Threshold ch 0-7)
##      "D98": even registers 16-30 (Trig Threshold ch 8-15)
##      "3D9": odd registers 1-15 (WBias ch 0-7)
##      "3D9": odd registers 17-31 (WBias ch 8-15)
##      misc: registers 48-55
##      misc: registers 56-63 (register 60 unused)
##      misc: registers 64-71
##      misc: registers 72-79
##
cmd_ASIC0_regs=""+\
"B0000"+TH+"B0020"+TH+"B0040"+TH+"B0060"+TH+"B0080"+TH+"B00A0"+TH+"B00C0"+TH+"B00E0"+TH+\
"B0100"+TH+"B0120"+TH+"B0140"+TH+"B0160"+TH+"B0180"+TH+"B01A0"+TH+"B01C0"+TH+"B01E0"+TH+\
"B00103D9"+"B00303D9"+"B00503D9"+"B00703D9"+"B00903D9"+"B00B03D9"+"B00D03D9"+"B00F03D9"+\
"B01103D9"+"B01303D9"+"B01503D9"+"B01703D9"+"B01903D9"+"B01B03D9"+"B01D03D9"+"B01F03D9"+\
"B0300514"+"B0310000"+"B0320A5A"+"B033044C"+"B03405DC"+"B0350426"+"B03604B9"+"B0370000"+\
"B0380480"+"B0390000"+"B03A08BB"+"B03B0000"+"B03D046A"+"B03E044C"+"B03F044C"+\
"B0400033"+"B0410007"+"B0420005"+"B0430019"+"B0440014"+"B0450028"+"B0460021"+"B0470035"+\
"B0480038"+"B049000C"+"B04A0028"+"B04B003A"+"B04C02E1"+"B04D0C28"+"B04E0480"+"B04F0AAA"
cmd_ASIC1_regs=""+\
"B1000"+TH+"B1020"+TH+"B1040"+TH+"B1060"+TH+"B1080"+TH+"B10A0"+TH+"B10C0"+TH+"B10E0"+TH+\
"B1100"+TH+"B1120"+TH+"B1140"+TH+"B1160"+TH+"B1180"+TH+"B11A0"+TH+"B11C0"+TH+"B11E0"+TH+\
"B10103D9"+"B10303D9"+"B10503D9"+"B10703D9"+"B10903D9"+"B10B03D9"+"B10D03D9"+"B10F03D9"+\
"B11103D9"+"B11303D9"+"B11503D9"+"B11703D9"+"B11903D9"+"B11B03D9"+"B11D03D9"+"B11F03D9"+\
"B1300514"+"B1310000"+"B1320A5A"+"B133044C"+"B13405DC"+"B1350426"+"B13604B9"+"B1370000"+\
"B1380480"+"B1390000"+"B13A08BB"+"B13B0000"+"B13D046A"+"B13E044C"+"B13F044C"+\
"B1400033"+"B1410007"+"B1420005"+"B1430019"+"B1440014"+"B1450028"+"B1460021"+"B1470035"+\
"B1480038"+"B149000C"+"B14A0028"+"B14B003A"+"B14C02E1"+"B14D0C28"+"B14E0480"+"B14F0AAA"
cmd_ASIC2_regs=""+\
"B2000"+TH+"B2020"+TH+"B2040"+TH+"B2060"+TH+"B2080"+TH+"B20A0"+TH+"B20C0"+TH+"B20E0"+TH+\
"B2100"+TH+"B2120"+TH+"B2140"+TH+"B2160"+TH+"B2180"+TH+"B21A0"+TH+"B21C0"+TH+"B21E0"+TH+\
"B20103D9"+"B20303D9"+"B20503D9"+"B20703D9"+"B20903D9"+"B20B03D9"+"B20D03D9"+"B20F03D9"+\
"B21103D9"+"B21303D9"+"B21503D9"+"B21703D9"+"B21903D9"+"B21B03D9"+"B21D03D9"+"B21F03D9"+\
"B2300514"+"B2310000"+"B2320A5A"+"B233044C"+"B23405DC"+"B2350426"+"B23604B9"+"B2370000"+\
"B2380480"+"B2390000"+"B23A08BB"+"B23B0000"+"B23D046A"+"B23E044C"+"B23F044C"+\
"B2400033"+"B2410007"+"B2420005"+"B2430019"+"B2440014"+"B2450028"+"B2460021"+"B2470035"+\
"B2480038"+"B249000C"+"B24A0028"+"B24B003A"+"B24C02E1"+"B24D0C28"+"B24E0480"+"B24F0AAA"
cmd_ASIC3_regs=""+\
"B3000"+TH+"B3020"+TH+"B3040"+TH+"B3060"+TH+"B3080"+TH+"B30A0"+TH+"B30C0"+TH+"B30E0"+TH+\
"B3100"+TH+"B3120"+TH+"B3140"+TH+"B3160"+TH+"B3180"+TH+"B31A0"+TH+"B31C0"+TH+"B31E0"+TH+\
"B30103D9"+"B30303D9"+"B30503D9"+"B30703D9"+"B30903D9"+"B30B03D9"+"B30D03D9"+"B30F03D9"+\
"B31103D9"+"B31303D9"+"B31503D9"+"B31703D9"+"B31903D9"+"B31B03D9"+"B31D03D9"+"B31F03D9"+\
"B3300514"+"B3310000"+"B3320A5A"+"B333044C"+"B33405DC"+"B3350426"+"B33604B9"+"B3370000"+\
"B3380480"+"B3390000"+"B33A08BB"+"B33B0000"+"B33D046A"+"B33E044C"+"B33F044C"+\
"B3400033"+"B3410007"+"B3420005"+"B3430019"+"B3440014"+"B3450028"+"B3460021"+"B3470035"+\
"B3480038"+"B349000C"+"B34A0028"+"B34B003A"+"B34C02E1"+"B34D0C28"+"B34E0480"+"B34F0AAA"
cmd_ASIC4_regs=""+\
"B4000"+TH+"B4020"+TH+"B4040"+TH+"B4060"+TH+"B4080"+TH+"B40A0"+TH+"B40C0"+TH+"B40E0"+TH+\
"B4100"+TH+"B4120"+TH+"B4140"+TH+"B4160"+TH+"B4180"+TH+"B41A0"+TH+"B41C0"+TH+"B41E0"+TH+\
"B40103D9"+"B40303D9"+"B40503D9"+"B40703D9"+"B40903D9"+"B40B03D9"+"B40D03D9"+"B40F03D9"+\
"B41103D9"+"B41303D9"+"B41503D9"+"B41703D9"+"B41903D9"+"B41B03D9"+"B41D03D9"+"B41F03D9"+\
"B4300514"+"B4310000"+"B4320A5A"+"B433044C"+"B43405DC"+"B4350426"+"B43604B9"+"B4370000"+\
"B4380480"+"B4390000"+"B43A08BB"+"B43B0000"+"B43D046A"+"B43E044C"+"B43F044C"+\
"B4400033"+"B4410007"+"B4420005"+"B4430019"+"B4440014"+"B4450028"+"B4460021"+"B4470035"+\
"B4480038"+"B449000C"+"B44A0028"+"B44B003A"+"B44C02E1"+"B44D0C28"+"B44E0480"+"B44F0AAA"
cmd_ASIC5_regs=""+\
"B5000"+TH+"B5020"+TH+"B5040"+TH+"B5060"+TH+"B5080"+TH+"B50A0"+TH+"B50C0"+TH+"B50E0"+TH+\
"B5100"+TH+"B5120"+TH+"B5140"+TH+"B5160"+TH+"B5180"+TH+"B51A0"+TH+"B51C0"+TH+"B51E0"+TH+\
"B50103D9"+"B50303D9"+"B50503D9"+"B50703D9"+"B50903D9"+"B50B03D9"+"B50D03D9"+"B50F03D9"+\
"B51103D9"+"B51303D9"+"B51503D9"+"B51703D9"+"B51903D9"+"B51B03D9"+"B51D03D9"+"B51F03D9"+\
"B5300514"+"B5310000"+"B5320A5A"+"B533044C"+"B53405DC"+"B5350426"+"B53604B9"+"B5370000"+\
"B5380480"+"B5390000"+"B53A08BB"+"B53B0000"+"B53D046A"+"B53E044C"+"B53F044C"+\
"B5400033"+"B5410007"+"B5420005"+"B5430019"+"B5440014"+"B5450028"+"B5460021"+"B5470035"+\
"B5480038"+"B549000C"+"B54A0028"+"B54B003A"+"B54C02E1"+"B54D0C28"+"B54E0480"+"B54F0AAA"
cmd_ASIC6_regs=""+\
"B6000"+TH+"B6020"+TH+"B6040"+TH+"B6060"+TH+"B6080"+TH+"B60A0"+TH+"B60C0"+TH+"B60E0"+TH+\
"B6100"+TH+"B6120"+TH+"B6140"+TH+"B6160"+TH+"B6180"+TH+"B61A0"+TH+"B61C0"+TH+"B61E0"+TH+\
"B60103D9"+"B60303D9"+"B60503D9"+"B60703D9"+"B60903D9"+"B60B03D9"+"B60D03D9"+"B60F03D9"+\
"B61103D9"+"B61303D9"+"B61503D9"+"B61703D9"+"B61903D9"+"B61B03D9"+"B61D03D9"+"B61F03D9"+\
"B6300514"+"B6310000"+"B6320A5A"+"B633044C"+"B63405DC"+"B6350426"+"B63604B9"+"B6370000"+\
"B6380480"+"B6390000"+"B63A08BB"+"B63B0000"+"B63D046A"+"B63E044C"+"B63F044C"+\
"B6400033"+"B6410007"+"B6420005"+"B6430019"+"B6440014"+"B6450028"+"B6460021"+"B6470035"+\
"B6480038"+"B649000C"+"B64A0028"+"B64B003A"+"B64C02E1"+"B64D0C28"+"B64E0480"+"B64F0AAA"
cmd_ASIC7_regs=""+\
"B7000"+TH+"B7020"+TH+"B7040"+TH+"B7060"+TH+"B7080"+TH+"B70A0"+TH+"B70C0"+TH+"B70E0"+TH+\
"B7100"+TH+"B7120"+TH+"B7140"+TH+"B7160"+TH+"B7180"+TH+"B71A0"+TH+"B71C0"+TH+"B71E0"+TH+\
"B70103D9"+"B70303D9"+"B70503D9"+"B70703D9"+"B70903D9"+"B70B03D9"+"B70D03D9"+"B70F03D9"+\
"B71103D9"+"B71303D9"+"B71503D9"+"B71703D9"+"B71903D9"+"B71B03D9"+"B71D03D9"+"B71F03D9"+\
"B7300514"+"B7310000"+"B7320A5A"+"B733044C"+"B73405DC"+"B7350426"+"B73604B9"+"B7370000"+\
"B7380480"+"B7390000"+"B73A08BB"+"B73B0000"+"B73D046A"+"B73E044C"+"B73F044C"+\
"B7400033"+"B7410007"+"B7420005"+"B7430019"+"B7440014"+"B7450028"+"B7460021"+"B7470035"+\
"B7480038"+"B749000C"+"B74A0028"+"B74B003A"+"B74C02E1"+"B74D0C28"+"B74E0480"+"B74F0AAA"
cmd_ASIC8_regs=""+\
"B8000"+TH+"B8020"+TH+"B8040"+TH+"B8060"+TH+"B8080"+TH+"B80A0"+TH+"B80C0"+TH+"B80E0"+TH+\
"B8100"+TH+"B8120"+TH+"B8140"+TH+"B8160"+TH+"B8180"+TH+"B81A0"+TH+"B81C0"+TH+"B81E0"+TH+\
"B80103D9"+"B80303D9"+"B80503D9"+"B80703D9"+"B80903D9"+"B80B03D9"+"B80D03D9"+"B80F03D9"+\
"B81103D9"+"B81303D9"+"B81503D9"+"B81703D9"+"B81903D9"+"B81B03D9"+"B81D03D9"+"B81F03D9"+\
"B8300514"+"B8310000"+"B8320A5A"+"B833044C"+"B83405DC"+"B8350426"+"B83604B9"+"B8370000"+\
"B8380480"+"B8390000"+"B83A08BB"+"B83B0000"+"B83D046A"+"B83E044C"+"B83F044C"+\
"B8400033"+"B8410007"+"B8420005"+"B8430019"+"B8440014"+"B8450028"+"B8460021"+"B8470035"+\
"B8480038"+"B849000C"+"B84A0028"+"B84B003A"+"B84C02E1"+"B84D0C28"+"B84E0480"+"B84F0AAA"
cmd_ASIC9_regs=""+\
"B9000"+TH+"B9020"+TH+"B9040"+TH+"B9060"+TH+"B9080"+TH+"B90A0"+TH+"B90C0"+TH+"B90E0"+TH+\
"B9100"+TH+"B9120"+TH+"B9140"+TH+"B9160"+TH+"B9180"+TH+"B91A0"+TH+"B91C0"+TH+"B91E0"+TH+\
"B90103D9"+"B90303D9"+"B90503D9"+"B90703D9"+"B90903D9"+"B90B03D9"+"B90D03D9"+"B90F03D9"+\
"B91103D9"+"B91303D9"+"B91503D9"+"B91703D9"+"B91903D9"+"B91B03D9"+"B91D03D9"+"B91F03D9"+\
"B9300514"+"B9310000"+"B9320A5A"+"B933044C"+"B93405DC"+"B9350426"+"B93604B9"+"B9370000"+\
"B9380480"+"B9390000"+"B93A08BB"+"B93B0000"+"B93D046A"+"B93E044C"+"B93F044C"+\
"B9400033"+"B9410007"+"B9420005"+"B9430019"+"B9440014"+"B9450028"+"B9460021"+"B9470035"+\
"B9480038"+"B949000C"+"B94A0028"+"B94B003A"+"B94C02E1"+"B94D0C28"+"B94E0480"+"B94F0AAA"

# Syntax: "C0=TrimDAC" + "ASIC" + "00" + "DAC setting (8 bit)"
cmd_HV_off = cmd_HV_on = syncwd
for ASIC in range(10):
    for CH in range (16):
        cmd_HV_off += hex( int('C',16)*(2**28) | ASIC*(2**20) | (CH)*(2**16) | 255 ).split('x')[1]
        cmd_HV_on  += hex( int('C',16)*(2**28) | ASIC*(2**20) | (CH)*(2**16) | 0   ).split('x')[1]

cmd_post=""+\
"01234567"+"AE000100"+\
"AF000000"+"AE000100"+\
"AF008000"+"AE000100"+"AE008000"+"AE000100"+"AE000100"+\
"AF00FFFF"+"AE000100"+"AE000100"+\
"AF008000"+"AE000100"+\
"AF050080"+"AE000100"+\
"AF060140"+"AE000100"+\
"AF140000"+"AE000100"+\
"AF1E0000"+"AE000100"+\
"AF1F0000"+"AE000100"+\
"AF320000"+"AE000100"+\
"AF2C0000"+"AE000100"+\
"AF2D0001"+"AE000100"+\
"AF2D0000"+"AE000100"+\
"AF330100"+"AE000100"+\
"AF340000"+"AE000100"+\
"AF350000"+"AE000100"+\
"AF360003"+"AE000100"+\
"AF370001"+"AE000100"+\
"AF370000"+"AE000100"+\
"AF380000"+"AE000100"+\
"AF390004"+"AE000100"+\
"AF3A0000"+"AE000100"+\
"AF4803FF"+"AE000100"+\
"AF3D0F00"+"AE000100"+\
"AF260000"+"AE000100"+\
"AF260800"+"AE000100"+\
"AF260000"+"AE000100"+\
"AF261080"+"AE000100"+\
"AF25C000"+"AE000100"+\
"AF4B0000"+"AE000100"+\
"AF4C0003"+"AE000100"+\
"AF270000"+"AE000100"+\
"AF0B0401"+"AE000100"+\
"AF0A0000"+"AE000100"+\
"AF0A0001"+"AE001000"+\
"AF0A0000"+"AE000100"+\
"AF3E0000"+"AE000100"+\
"AF460000"+"AE000100"+\
"AF470000"+"AE000100"+\
"AF470001"+"AE000100"+\
"AF470000"+"AE000100"+\
"AF460001"+"AE000100"+\
"AF270000"+"AE000100"+\
"AF4D0450"+"AE000100"+\
"AF4DC450"+"AE000100"+\
"AF008D0E"+"AE000100"

#ctrl.KLMprint(cmd_pre, "cmd_pre")
ctrl.send(syncwd+cmd_pre)
time.sleep(.1)

#ctrl.KLMprint(cmd_ASIC0, "cmd_ASIC0")
ctrl.send(syncwd+cmd_ASIC0_regs)
time.sleep(.3)
ctrl.send(syncwd+cmd_ASIC1_regs)
time.sleep(.3)
ctrl.send(syncwd+cmd_ASIC2_regs)
time.sleep(.3)
ctrl.send(syncwd+cmd_ASIC3_regs)
time.sleep(.3)
ctrl.send(syncwd+cmd_ASIC4_regs)
time.sleep(.3)
ctrl.send(syncwd+cmd_ASIC5_regs)
time.sleep(.3)
ctrl.send(syncwd+cmd_ASIC6_regs)
time.sleep(.3)
ctrl.send(syncwd+cmd_ASIC7_regs)
time.sleep(.3)
ctrl.send(syncwd+cmd_ASIC8_regs)
time.sleep(.3)
ctrl.send(syncwd+cmd_ASIC9_regs)
time.sleep(.3)

#ctrl.KLMprint(cmd_HV_on, "cmd_HV_on")
ctrl.send(syncwd+cmd_HV_on)
time.sleep(.3)

#ctrl.KLMprint(cmd_post, "cmd_post")
ctrl.send(syncwd+cmd_post)
time.sleep(.1)

ctrl.close()