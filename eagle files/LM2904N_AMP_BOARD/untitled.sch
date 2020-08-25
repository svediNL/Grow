<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="8.4.1">
<drawing>
<settings>
<setting alwaysvectorfont="yes"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="24" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="88" name="SimResults" color="9" fill="1" visible="yes" active="yes"/>
<layer number="89" name="SimProbes" color="9" fill="1" visible="yes" active="yes"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="myLamp">
<packages>
<package name="LM2904">
<pad name="OUTA" x="0" y="0" drill="0.9" shape="long" rot="R90"/>
<pad name="A-" x="2.54" y="0" drill="0.9" shape="long" rot="R270"/>
<pad name="A+" x="5.08" y="0" drill="0.9" shape="long" rot="R90"/>
<pad name="GND" x="7.62" y="0" drill="0.9" shape="long" rot="R90"/>
<pad name="VIN" x="0" y="8.255" drill="0.9" shape="long" rot="R90"/>
<pad name="OUTB" x="2.54" y="8.255" drill="0.9" shape="long" rot="R90"/>
<pad name="B-" x="5.08" y="8.255" drill="0.9" shape="long" rot="R90"/>
<pad name="B+" x="7.62" y="8.255" drill="0.9" shape="long" rot="R90"/>
<text x="0.635" y="3.81" size="1.27" layer="21" font="fixed" ratio="15">LM2904</text>
<text x="-3.81" y="0.635" size="1.27" layer="21" font="fixed" ratio="15" rot="R90">&gt;NAME</text>
<wire x1="-2.54" y1="8.255" x2="-2.54" y2="6.35" width="0.2" layer="21"/>
<wire x1="-2.54" y1="6.35" x2="-2.54" y2="2.54" width="0.2" layer="21"/>
<wire x1="-2.54" y1="2.54" x2="-2.54" y2="0" width="0.2" layer="21"/>
<wire x1="-2.54" y1="6.35" x2="-0.635" y2="4.445" width="0.2" layer="21" curve="-90"/>
<wire x1="-0.635" y1="4.445" x2="-2.54" y2="2.54" width="0.2" layer="21" curve="-90"/>
<wire x1="10.16" y1="8.255" x2="10.16" y2="0" width="0.2" layer="21"/>
</package>
<package name="RESISTOR">
<pad name="P$1" x="0" y="0" drill="0.6" diameter="1.4224"/>
<pad name="P$2" x="16.51" y="0" drill="0.6" diameter="1.4224"/>
<wire x1="5.08" y1="-1.27" x2="11.43" y2="-1.27" width="0.127" layer="22"/>
<wire x1="11.43" y1="-1.27" x2="11.43" y2="0" width="0.127" layer="22"/>
<wire x1="11.43" y1="0" x2="11.43" y2="1.27" width="0.127" layer="22"/>
<wire x1="11.43" y1="1.27" x2="5.08" y2="1.27" width="0.127" layer="22"/>
<wire x1="5.08" y1="1.27" x2="5.08" y2="0" width="0.127" layer="22"/>
<wire x1="5.08" y1="0" x2="5.08" y2="-1.27" width="0.127" layer="22"/>
<wire x1="1.27" y1="0" x2="5.08" y2="0" width="0.127" layer="22"/>
<wire x1="11.43" y1="0" x2="15.24" y2="0" width="0.127" layer="22"/>
<text x="3.81" y="2.54" size="1.27" layer="26" font="vector" ratio="15" distance="65">&gt;NAME</text>
</package>
<package name="BRIDGE">
<pad name="P$1" x="0" y="0" drill="0.6" diameter="1.4224" shape="offset"/>
<pad name="P$2" x="4.572" y="0" drill="0.6" diameter="1.4224" shape="offset" rot="R180"/>
</package>
<package name="1X02">
<description>&lt;b&gt;PIN HEADER&lt;/b&gt;</description>
<wire x1="-1.905" y1="1.27" x2="-0.635" y2="1.27" width="0.1524" layer="21"/>
<wire x1="-0.635" y1="1.27" x2="0" y2="0.635" width="0.1524" layer="21"/>
<wire x1="0" y1="0.635" x2="0" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="0" y1="-0.635" x2="-0.635" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="-2.54" y1="0.635" x2="-2.54" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="-1.905" y1="1.27" x2="-2.54" y2="0.635" width="0.1524" layer="21"/>
<wire x1="-2.54" y1="-0.635" x2="-1.905" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="-0.635" y1="-1.27" x2="-1.905" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="0" y1="0.635" x2="0.635" y2="1.27" width="0.1524" layer="21"/>
<wire x1="0.635" y1="1.27" x2="1.905" y2="1.27" width="0.1524" layer="21"/>
<wire x1="1.905" y1="1.27" x2="2.54" y2="0.635" width="0.1524" layer="21"/>
<wire x1="2.54" y1="0.635" x2="2.54" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="2.54" y1="-0.635" x2="1.905" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="1.905" y1="-1.27" x2="0.635" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="0.635" y1="-1.27" x2="0" y2="-0.635" width="0.1524" layer="21"/>
<pad name="1" x="-1.27" y="0" drill="1.4" shape="long" rot="R90"/>
<pad name="2" x="1.27" y="0" drill="1.4" shape="long" rot="R90"/>
<text x="-2.6162" y="1.8288" size="1.27" layer="25" font="vector" ratio="14">&gt;NAME</text>
<text x="-2.54" y="-3.175" size="1.27" layer="27" font="vector" ratio="14">&gt;VALUE</text>
<rectangle x1="-1.524" y1="-0.254" x2="-1.016" y2="0.254" layer="51"/>
<rectangle x1="1.016" y1="-0.254" x2="1.524" y2="0.254" layer="51"/>
</package>
<package name="1X02/90">
<description>&lt;b&gt;PIN HEADER&lt;/b&gt;</description>
<wire x1="-2.54" y1="-1.905" x2="0" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="0" y1="-1.905" x2="0" y2="0.635" width="0.1524" layer="21"/>
<wire x1="0" y1="0.635" x2="-2.54" y2="0.635" width="0.1524" layer="21"/>
<wire x1="-2.54" y1="0.635" x2="-2.54" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="-1.27" y1="6.985" x2="-1.27" y2="1.27" width="0.762" layer="21"/>
<wire x1="0" y1="-1.905" x2="2.54" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="2.54" y1="-1.905" x2="2.54" y2="0.635" width="0.1524" layer="21"/>
<wire x1="2.54" y1="0.635" x2="0" y2="0.635" width="0.1524" layer="21"/>
<wire x1="1.27" y1="6.985" x2="1.27" y2="1.27" width="0.762" layer="21"/>
<pad name="1" x="-1.27" y="-3.81" drill="1.016" shape="long" rot="R90"/>
<pad name="2" x="1.27" y="-3.81" drill="1.016" shape="long" rot="R90"/>
<text x="-3.175" y="-3.81" size="1.27" layer="25" ratio="10" rot="R90">&gt;NAME</text>
<text x="4.445" y="-3.81" size="1.27" layer="27" rot="R90">&gt;VALUE</text>
<rectangle x1="-1.651" y1="0.635" x2="-0.889" y2="1.143" layer="21"/>
<rectangle x1="0.889" y1="0.635" x2="1.651" y2="1.143" layer="21"/>
<rectangle x1="-1.651" y1="-2.921" x2="-0.889" y2="-1.905" layer="21"/>
<rectangle x1="0.889" y1="-2.921" x2="1.651" y2="-1.905" layer="21"/>
</package>
<package name="1X03">
<description>&lt;b&gt;PIN HEADER&lt;/b&gt;</description>
<wire x1="-3.175" y1="1.27" x2="-1.905" y2="1.27" width="0.1524" layer="21"/>
<wire x1="-1.905" y1="1.27" x2="-1.27" y2="0.635" width="0.1524" layer="21"/>
<wire x1="-1.27" y1="0.635" x2="-1.27" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="-1.27" y1="-0.635" x2="-1.905" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="-1.27" y1="0.635" x2="-0.635" y2="1.27" width="0.1524" layer="21"/>
<wire x1="-0.635" y1="1.27" x2="0.635" y2="1.27" width="0.1524" layer="21"/>
<wire x1="0.635" y1="1.27" x2="1.27" y2="0.635" width="0.1524" layer="21"/>
<wire x1="1.27" y1="0.635" x2="1.27" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="1.27" y1="-0.635" x2="0.635" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="0.635" y1="-1.27" x2="-0.635" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="-0.635" y1="-1.27" x2="-1.27" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="-3.81" y1="0.635" x2="-3.81" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="-3.175" y1="1.27" x2="-3.81" y2="0.635" width="0.1524" layer="21"/>
<wire x1="-3.81" y1="-0.635" x2="-3.175" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="-1.905" y1="-1.27" x2="-3.175" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="1.27" y1="0.635" x2="1.905" y2="1.27" width="0.1524" layer="21"/>
<wire x1="1.905" y1="1.27" x2="3.175" y2="1.27" width="0.1524" layer="21"/>
<wire x1="3.175" y1="1.27" x2="3.81" y2="0.635" width="0.1524" layer="21"/>
<wire x1="3.81" y1="0.635" x2="3.81" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="3.81" y1="-0.635" x2="3.175" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="3.175" y1="-1.27" x2="1.905" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="1.905" y1="-1.27" x2="1.27" y2="-0.635" width="0.1524" layer="21"/>
<pad name="1" x="-2.54" y="0" drill="1.4" shape="long" rot="R90"/>
<pad name="2" x="0" y="0" drill="1.4" shape="long" rot="R90"/>
<pad name="3" x="2.54" y="0" drill="1.4" shape="long" rot="R90"/>
<text x="-3.8862" y="2.4638" size="1.27" layer="25" font="vector" ratio="14">&gt;NAME</text>
<text x="-3.81" y="-3.81" size="1.27" layer="27" font="vector" ratio="14">&gt;VALUE</text>
<rectangle x1="-0.254" y1="-0.254" x2="0.254" y2="0.254" layer="51"/>
<rectangle x1="-2.794" y1="-0.254" x2="-2.286" y2="0.254" layer="51"/>
<rectangle x1="2.286" y1="-0.254" x2="2.794" y2="0.254" layer="51"/>
</package>
<package name="1X03/90">
<description>&lt;b&gt;PIN HEADER&lt;/b&gt;</description>
<wire x1="-3.81" y1="-1.905" x2="-1.27" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="-1.27" y1="-1.905" x2="-1.27" y2="0.635" width="0.1524" layer="21"/>
<wire x1="-1.27" y1="0.635" x2="-3.81" y2="0.635" width="0.1524" layer="21"/>
<wire x1="-3.81" y1="0.635" x2="-3.81" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="-2.54" y1="6.985" x2="-2.54" y2="1.27" width="0.762" layer="21"/>
<wire x1="-1.27" y1="-1.905" x2="1.27" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="1.27" y1="-1.905" x2="1.27" y2="0.635" width="0.1524" layer="21"/>
<wire x1="1.27" y1="0.635" x2="-1.27" y2="0.635" width="0.1524" layer="21"/>
<wire x1="0" y1="6.985" x2="0" y2="1.27" width="0.762" layer="21"/>
<wire x1="1.27" y1="-1.905" x2="3.81" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="3.81" y1="-1.905" x2="3.81" y2="0.635" width="0.1524" layer="21"/>
<wire x1="3.81" y1="0.635" x2="1.27" y2="0.635" width="0.1524" layer="21"/>
<wire x1="2.54" y1="6.985" x2="2.54" y2="1.27" width="0.762" layer="21"/>
<pad name="1" x="-2.54" y="-3.81" drill="1.016" shape="long" rot="R90"/>
<pad name="2" x="0" y="-3.81" drill="1.016" shape="long" rot="R90"/>
<pad name="3" x="2.54" y="-3.81" drill="1.016" shape="long" rot="R90"/>
<text x="-4.445" y="-3.81" size="1.27" layer="25" ratio="10" rot="R90">&gt;NAME</text>
<text x="5.715" y="-3.81" size="1.27" layer="27" rot="R90">&gt;VALUE</text>
<rectangle x1="-2.921" y1="0.635" x2="-2.159" y2="1.143" layer="21"/>
<rectangle x1="-0.381" y1="0.635" x2="0.381" y2="1.143" layer="21"/>
<rectangle x1="2.159" y1="0.635" x2="2.921" y2="1.143" layer="21"/>
<rectangle x1="-2.921" y1="-2.921" x2="-2.159" y2="-1.905" layer="21"/>
<rectangle x1="-0.381" y1="-2.921" x2="0.381" y2="-1.905" layer="21"/>
<rectangle x1="2.159" y1="-2.921" x2="2.921" y2="-1.905" layer="21"/>
</package>
</packages>
<symbols>
<symbol name="LM2904">
<pin name="P$1" x="-12.7" y="25.4" visible="pad" length="short"/>
<pin name="P$2" x="-12.7" y="7.62" visible="pad" length="short"/>
<pin name="P$3" x="-12.7" y="2.54" visible="pad" length="short"/>
<pin name="P$4" x="25.4" y="5.08" visible="pad" length="short" rot="R180"/>
<pin name="P$5" x="25.4" y="27.94" visible="pad" length="short" rot="R180"/>
<pin name="P$6" x="25.4" y="22.86" visible="pad" length="short" rot="R180"/>
<pin name="P$7" x="-12.7" y="29.21" visible="pad" length="short"/>
<pin name="P$8" x="25.4" y="1.27" visible="pad" length="short" rot="R180"/>
<wire x1="-2.54" y1="20.32" x2="-7.62" y2="10.16" width="0.254" layer="94"/>
<wire x1="-7.62" y1="10.16" x2="-5.08" y2="10.16" width="0.254" layer="94"/>
<wire x1="-5.08" y1="10.16" x2="0" y2="10.16" width="0.254" layer="94"/>
<wire x1="0" y1="10.16" x2="2.54" y2="10.16" width="0.254" layer="94"/>
<wire x1="2.54" y1="10.16" x2="1.27" y2="12.7" width="0.254" layer="94"/>
<wire x1="1.27" y1="12.7" x2="-1.27" y2="17.78" width="0.254" layer="94"/>
<wire x1="-1.27" y1="17.78" x2="-2.54" y2="20.32" width="0.254" layer="94"/>
<wire x1="10.16" y1="20.32" x2="11.43" y2="17.78" width="0.254" layer="94"/>
<wire x1="11.43" y1="17.78" x2="13.97" y2="12.7" width="0.254" layer="94"/>
<wire x1="13.97" y1="12.7" x2="15.24" y2="10.16" width="0.254" layer="94"/>
<wire x1="15.24" y1="10.16" x2="20.32" y2="20.32" width="0.254" layer="94"/>
<wire x1="20.32" y1="20.32" x2="17.78" y2="20.32" width="0.254" layer="94"/>
<wire x1="17.78" y1="20.32" x2="12.7" y2="20.32" width="0.254" layer="94"/>
<wire x1="12.7" y1="20.32" x2="10.16" y2="20.32" width="0.254" layer="94"/>
<wire x1="-2.54" y1="20.32" x2="-2.54" y2="25.4" width="0.254" layer="94"/>
<wire x1="-2.54" y1="25.4" x2="-10.16" y2="25.4" width="0.254" layer="94"/>
<wire x1="-5.08" y1="10.16" x2="-5.08" y2="7.62" width="0.254" layer="94"/>
<wire x1="-5.08" y1="7.62" x2="-10.16" y2="7.62" width="0.254" layer="94"/>
<wire x1="0" y1="10.16" x2="0" y2="2.54" width="0.254" layer="94"/>
<wire x1="0" y1="2.54" x2="-10.16" y2="2.54" width="0.254" layer="94"/>
<wire x1="15.24" y1="10.16" x2="15.24" y2="5.08" width="0.254" layer="94"/>
<wire x1="15.24" y1="5.08" x2="22.86" y2="5.08" width="0.254" layer="94"/>
<wire x1="17.78" y1="20.32" x2="17.78" y2="22.86" width="0.254" layer="94"/>
<wire x1="17.78" y1="22.86" x2="22.86" y2="22.86" width="0.254" layer="94"/>
<wire x1="12.7" y1="20.32" x2="12.7" y2="27.94" width="0.254" layer="94"/>
<wire x1="12.7" y1="27.94" x2="22.86" y2="27.94" width="0.254" layer="94"/>
<wire x1="1.27" y1="12.7" x2="6.985" y2="12.7" width="0.254" layer="94"/>
<wire x1="6.985" y1="12.7" x2="13.97" y2="12.7" width="0.254" layer="94"/>
<wire x1="11.43" y1="17.78" x2="5.08" y2="17.78" width="0.254" layer="94"/>
<text x="-1.27" y="10.795" size="2.54" layer="94">+</text>
<text x="12.065" y="17.78" size="2.54" layer="94">+</text>
<text x="17.145" y="17.78" size="2.54" layer="94">-</text>
<text x="-5.715" y="10.795" size="2.54" layer="94">-</text>
<wire x1="5.08" y1="17.78" x2="-1.27" y2="17.78" width="0.254" layer="94"/>
<wire x1="5.08" y1="17.78" x2="5.08" y2="29.21" width="0.254" layer="94"/>
<wire x1="5.08" y1="29.21" x2="-10.16" y2="29.21" width="0.254" layer="94"/>
<wire x1="6.985" y1="12.7" x2="6.985" y2="1.27" width="0.254" layer="94"/>
<wire x1="6.985" y1="1.27" x2="22.86" y2="1.27" width="0.254" layer="94"/>
<wire x1="-10.16" y1="38.1" x2="-10.16" y2="-1.27" width="0.254" layer="94"/>
<wire x1="-10.16" y1="-1.27" x2="22.86" y2="-1.27" width="0.254" layer="94"/>
<wire x1="22.86" y1="-1.27" x2="22.86" y2="1.27" width="0.254" layer="94"/>
<wire x1="22.86" y1="1.27" x2="22.86" y2="38.1" width="0.254" layer="94"/>
<wire x1="22.86" y1="38.1" x2="-10.16" y2="38.1" width="0.254" layer="94"/>
<text x="-8.255" y="34.29" size="2.54" layer="94">LM2904</text>
<text x="-10.16" y="39.37" size="2.54" layer="95">&gt;NAME</text>
</symbol>
<symbol name="RESISTOR">
<pin name="P$1" x="0" y="0" visible="off" length="point"/>
<pin name="P$2" x="10.16" y="0" visible="off" length="point" rot="R180"/>
<wire x1="2.032" y1="0" x2="2.794" y2="0.762" width="0.254" layer="94"/>
<wire x1="2.794" y1="0.762" x2="4.318" y2="-0.762" width="0.254" layer="94"/>
<wire x1="4.318" y1="-0.762" x2="5.842" y2="0.762" width="0.254" layer="94"/>
<wire x1="5.842" y1="0.762" x2="7.366" y2="-0.762" width="0.254" layer="94"/>
<wire x1="7.366" y1="-0.762" x2="8.128" y2="0" width="0.254" layer="94"/>
<wire x1="0" y1="0" x2="2.032" y2="0" width="0.254" layer="94"/>
<wire x1="8.128" y1="0" x2="10.16" y2="0" width="0.254" layer="94"/>
<text x="0" y="2.032" size="1.016" layer="94">&gt;NAME</text>
</symbol>
<symbol name="BRIDGE">
<pin name="P$1" x="0" y="0" visible="off" length="short"/>
<pin name="P$2" x="10.16" y="0" visible="off" length="short" rot="R180"/>
<wire x1="1.27" y1="1.27" x2="8.89" y2="1.27" width="0.254" layer="94"/>
<text x="2.54" y="-2.54" size="1.27" layer="94">BRIDGE</text>
</symbol>
<symbol name="PINHD2">
<wire x1="-6.35" y1="-2.54" x2="1.27" y2="-2.54" width="0.4064" layer="94"/>
<wire x1="1.27" y1="-2.54" x2="1.27" y2="5.08" width="0.4064" layer="94"/>
<wire x1="1.27" y1="5.08" x2="-6.35" y2="5.08" width="0.4064" layer="94"/>
<wire x1="-6.35" y1="5.08" x2="-6.35" y2="-2.54" width="0.4064" layer="94"/>
<text x="-6.35" y="5.715" size="1.778" layer="95">&gt;NAME</text>
<text x="-6.35" y="-5.08" size="1.778" layer="96">&gt;VALUE</text>
<pin name="1" x="-2.54" y="2.54" visible="pad" length="short" direction="pas" function="dot"/>
<pin name="2" x="-2.54" y="0" visible="pad" length="short" direction="pas" function="dot"/>
</symbol>
<symbol name="PINHD3">
<wire x1="-6.35" y1="-5.08" x2="1.27" y2="-5.08" width="0.4064" layer="94"/>
<wire x1="1.27" y1="-5.08" x2="1.27" y2="5.08" width="0.4064" layer="94"/>
<wire x1="1.27" y1="5.08" x2="-6.35" y2="5.08" width="0.4064" layer="94"/>
<wire x1="-6.35" y1="5.08" x2="-6.35" y2="-5.08" width="0.4064" layer="94"/>
<text x="-6.35" y="5.715" size="1.778" layer="95">&gt;NAME</text>
<text x="-6.35" y="-7.62" size="1.778" layer="96">&gt;VALUE</text>
<pin name="1" x="-2.54" y="2.54" visible="pad" length="short" direction="pas" function="dot"/>
<pin name="2" x="-2.54" y="0" visible="pad" length="short" direction="pas" function="dot"/>
<pin name="3" x="-2.54" y="-2.54" visible="pad" length="short" direction="pas" function="dot"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="LM2904">
<gates>
<gate name="G$1" symbol="LM2904" x="-5.08" y="-15.24"/>
</gates>
<devices>
<device name="" package="LM2904">
<connects>
<connect gate="G$1" pin="P$1" pad="OUTA"/>
<connect gate="G$1" pin="P$2" pad="A-"/>
<connect gate="G$1" pin="P$3" pad="A+"/>
<connect gate="G$1" pin="P$4" pad="OUTB"/>
<connect gate="G$1" pin="P$5" pad="B+"/>
<connect gate="G$1" pin="P$6" pad="B-"/>
<connect gate="G$1" pin="P$7" pad="VIN"/>
<connect gate="G$1" pin="P$8" pad="GND"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="RESISTOR">
<gates>
<gate name="G$1" symbol="RESISTOR" x="0" y="0"/>
</gates>
<devices>
<device name="" package="RESISTOR">
<connects>
<connect gate="G$1" pin="P$1" pad="P$1"/>
<connect gate="G$1" pin="P$2" pad="P$2"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="BRIDGE">
<gates>
<gate name="G$1" symbol="BRIDGE" x="0" y="0"/>
</gates>
<devices>
<device name="" package="BRIDGE">
<connects>
<connect gate="G$1" pin="P$1" pad="P$1"/>
<connect gate="G$1" pin="P$2" pad="P$2"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="PINHD-1X2" prefix="JP" uservalue="yes">
<description>&lt;b&gt;PIN HEADER&lt;/b&gt;</description>
<gates>
<gate name="G$1" symbol="PINHD2" x="0" y="0"/>
</gates>
<devices>
<device name="" package="1X02">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="/90" package="1X02/90">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="PINHD-1X3" prefix="JP" uservalue="yes">
<description>&lt;b&gt;PIN HEADER&lt;/b&gt;</description>
<gates>
<gate name="A" symbol="PINHD3" x="0" y="0"/>
</gates>
<devices>
<device name="" package="1X03">
<connects>
<connect gate="A" pin="1" pad="1"/>
<connect gate="A" pin="2" pad="2"/>
<connect gate="A" pin="3" pad="3"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="/90" package="1X03/90">
<connects>
<connect gate="A" pin="1" pad="1"/>
<connect gate="A" pin="2" pad="2"/>
<connect gate="A" pin="3" pad="3"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="supply2" urn="urn:adsk.eagle:library:372">
<description>&lt;b&gt;Supply Symbols&lt;/b&gt;&lt;p&gt;
GND, VCC, 0V, +5V, -5V, etc.&lt;p&gt;
Please keep in mind, that these devices are necessary for the
automatic wiring of the supply signals.&lt;p&gt;
The pin name defined in the symbol is identical to the net which is to be wired automatically.&lt;p&gt;
In this library the device names are the same as the pin names of the symbols, therefore the correct signal names appear next to the supply symbols in the schematic.&lt;p&gt;
&lt;author&gt;Created by librarian@cadsoft.de&lt;/author&gt;</description>
<packages>
</packages>
<symbols>
<symbol name="+12V" urn="urn:adsk.eagle:symbol:26985/1" library_version="2">
<wire x1="0" y1="1.905" x2="0" y2="0.635" width="0.1524" layer="94"/>
<wire x1="-0.635" y1="1.27" x2="0.635" y2="1.27" width="0.1524" layer="94"/>
<circle x="0" y="1.27" radius="1.27" width="0.254" layer="94"/>
<text x="-2.54" y="3.175" size="1.778" layer="96">&gt;VALUE</text>
<pin name="+12V" x="0" y="-2.54" visible="off" length="short" direction="sup" rot="R90"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="+12V" urn="urn:adsk.eagle:component:27033/1" prefix="SUPPLY" library_version="2">
<description>&lt;b&gt;SUPPLY SYMBOL&lt;/b&gt;</description>
<gates>
<gate name="+12V" symbol="+12V" x="0" y="0"/>
</gates>
<devices>
<device name="">
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="U$1" library="myLamp" deviceset="LM2904" device=""/>
<part name="SUPPLY1" library="supply2" library_urn="urn:adsk.eagle:library:372" deviceset="+12V" device=""/>
<part name="A_OUT" library="myLamp" deviceset="PINHD-1X2" device=""/>
<part name="B_IN" library="myLamp" deviceset="PINHD-1X2" device=""/>
<part name="V_SOURCE" library="myLamp" deviceset="PINHD-1X3" device=""/>
<part name="A_IN" library="myLamp" deviceset="PINHD-1X2" device=""/>
<part name="B_OUT" library="myLamp" deviceset="PINHD-1X2" device=""/>
<part name="RF_A" library="myLamp" deviceset="RESISTOR" device=""/>
<part name="RF_B" library="myLamp" deviceset="RESISTOR" device=""/>
<part name="R1_A" library="myLamp" deviceset="RESISTOR" device=""/>
<part name="R1_B" library="myLamp" deviceset="RESISTOR" device=""/>
<part name="U$2" library="myLamp" deviceset="BRIDGE" device=""/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="U$1" gate="G$1" x="48.26" y="25.4"/>
<instance part="SUPPLY1" gate="+12V" x="25.4" y="58.42"/>
<instance part="A_OUT" gate="G$1" x="45.72" y="88.9" rot="R180"/>
<instance part="B_IN" gate="G$1" x="45.72" y="73.66" rot="R180"/>
<instance part="V_SOURCE" gate="A" x="0" y="88.9" rot="R180"/>
<instance part="A_IN" gate="G$1" x="0" y="73.66" rot="R180"/>
<instance part="B_OUT" gate="G$1" x="86.36" y="88.9" rot="R180"/>
<instance part="RF_A" gate="G$1" x="30.48" y="38.1" rot="R90"/>
<instance part="RF_B" gate="G$1" x="78.74" y="45.72" rot="R270"/>
<instance part="R1_A" gate="G$1" x="17.78" y="33.02"/>
<instance part="R1_B" gate="G$1" x="91.44" y="48.26" rot="R180"/>
<instance part="U$2" gate="G$1" x="88.9" y="20.32"/>
</instances>
<busses>
</busses>
<nets>
<net name="+12V" class="0">
<segment>
<pinref part="SUPPLY1" gate="+12V" pin="+12V"/>
<pinref part="U$1" gate="G$1" pin="P$7"/>
<wire x1="25.4" y1="55.88" x2="25.4" y2="54.61" width="0.1524" layer="91"/>
<wire x1="25.4" y1="54.61" x2="35.56" y2="54.61" width="0.1524" layer="91"/>
</segment>
<segment>
<pinref part="V_SOURCE" gate="A" pin="2"/>
<wire x1="2.54" y1="88.9" x2="15.24" y2="88.9" width="0.1524" layer="91"/>
<label x="10.16" y="88.9" size="1.778" layer="95"/>
</segment>
</net>
<net name="GND1" class="0">
<segment>
<pinref part="V_SOURCE" gate="A" pin="1"/>
<wire x1="2.54" y1="86.36" x2="15.24" y2="86.36" width="0.1524" layer="91"/>
<label x="10.16" y="83.82" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="A_OUT" gate="G$1" pin="1"/>
<wire x1="48.26" y1="86.36" x2="60.96" y2="86.36" width="0.1524" layer="91"/>
<label x="58.42" y="83.82" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="B_OUT" gate="G$1" pin="1"/>
<wire x1="88.9" y1="86.36" x2="101.6" y2="86.36" width="0.1524" layer="91"/>
<label x="99.06" y="83.82" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$2" gate="G$1" pin="P$2"/>
<wire x1="99.06" y1="20.32" x2="106.68" y2="20.32" width="0.1524" layer="91"/>
<label x="104.14" y="20.32" size="1.778" layer="95"/>
</segment>
</net>
<net name="GND" class="0">
<segment>
<pinref part="A_IN" gate="G$1" pin="2"/>
<wire x1="2.54" y1="73.66" x2="15.24" y2="73.66" width="0.1524" layer="91"/>
<label x="10.16" y="73.66" size="1.778" layer="95"/>
</segment>
</net>
<net name="A_OUT" class="0">
<segment>
<pinref part="A_OUT" gate="G$1" pin="2"/>
<wire x1="48.26" y1="88.9" x2="60.96" y2="88.9" width="0.1524" layer="91"/>
<label x="58.42" y="88.9" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$1" gate="G$1" pin="P$1"/>
<wire x1="35.56" y1="50.8" x2="30.48" y2="50.8" width="0.1524" layer="91"/>
<wire x1="30.48" y1="48.26" x2="30.48" y2="50.8" width="0.1524" layer="91"/>
<wire x1="30.48" y1="50.8" x2="17.78" y2="50.8" width="0.1524" layer="91"/>
<junction x="30.48" y="50.8"/>
<label x="15.24" y="50.8" size="1.778" layer="95"/>
<pinref part="RF_A" gate="G$1" pin="P$2"/>
</segment>
</net>
<net name="B_SIG" class="0">
<segment>
<pinref part="B_IN" gate="G$1" pin="2"/>
<wire x1="48.26" y1="73.66" x2="60.96" y2="73.66" width="0.1524" layer="91"/>
<label x="55.88" y="73.66" size="1.778" layer="95"/>
</segment>
</net>
<net name="B_OUT" class="0">
<segment>
<pinref part="B_OUT" gate="G$1" pin="2"/>
<wire x1="88.9" y1="88.9" x2="101.6" y2="88.9" width="0.1524" layer="91"/>
<label x="99.06" y="88.9" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$1" gate="G$1" pin="P$4"/>
<wire x1="73.66" y1="30.48" x2="78.74" y2="30.48" width="0.1524" layer="91"/>
<wire x1="78.74" y1="35.56" x2="78.74" y2="30.48" width="0.1524" layer="91"/>
<wire x1="78.74" y1="30.48" x2="88.9" y2="30.48" width="0.1524" layer="91"/>
<junction x="78.74" y="30.48"/>
<label x="88.9" y="30.48" size="1.778" layer="95"/>
<pinref part="RF_B" gate="G$1" pin="P$2"/>
</segment>
</net>
<net name="B_GND" class="0">
<segment>
<pinref part="B_IN" gate="G$1" pin="1"/>
<wire x1="48.26" y1="71.12" x2="60.96" y2="71.12" width="0.1524" layer="91"/>
<label x="55.88" y="68.58" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$3" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="P$6"/>
<wire x1="73.66" y1="48.26" x2="78.74" y2="48.26" width="0.1524" layer="91"/>
<wire x1="78.74" y1="48.26" x2="81.28" y2="48.26" width="0.1524" layer="91"/>
<wire x1="78.74" y1="45.72" x2="78.74" y2="48.26" width="0.1524" layer="91"/>
<junction x="78.74" y="48.26"/>
<pinref part="R1_B" gate="G$1" pin="P$2"/>
<pinref part="RF_B" gate="G$1" pin="P$1"/>
</segment>
</net>
<net name="N$4" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="P$2"/>
<wire x1="27.94" y1="33.02" x2="30.48" y2="33.02" width="0.1524" layer="91"/>
<wire x1="30.48" y1="33.02" x2="35.56" y2="33.02" width="0.1524" layer="91"/>
<wire x1="30.48" y1="38.1" x2="30.48" y2="33.02" width="0.1524" layer="91"/>
<junction x="30.48" y="33.02"/>
<pinref part="RF_A" gate="G$1" pin="P$1"/>
<pinref part="R1_A" gate="G$1" pin="P$2"/>
</segment>
</net>
<net name="A+" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="P$3"/>
<wire x1="35.56" y1="27.94" x2="12.7" y2="27.94" width="0.1524" layer="91"/>
<label x="17.78" y="27.94" size="1.778" layer="95"/>
</segment>
</net>
<net name="A-" class="0">
<segment>
<wire x1="17.78" y1="33.02" x2="10.16" y2="33.02" width="0.1524" layer="91"/>
<label x="12.7" y="33.02" size="1.778" layer="95"/>
<pinref part="R1_A" gate="G$1" pin="P$1"/>
</segment>
</net>
<net name="B-" class="0">
<segment>
<wire x1="91.44" y1="48.26" x2="96.52" y2="48.26" width="0.1524" layer="91"/>
<label x="96.52" y="48.26" size="1.778" layer="95"/>
<pinref part="R1_B" gate="G$1" pin="P$1"/>
</segment>
</net>
<net name="B+" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="P$5"/>
<wire x1="73.66" y1="53.34" x2="93.98" y2="53.34" width="0.1524" layer="91"/>
<label x="93.98" y="53.34" size="1.778" layer="95"/>
</segment>
</net>
<net name="A_GND" class="0">
<segment>
<pinref part="A_IN" gate="G$1" pin="1"/>
<wire x1="2.54" y1="71.12" x2="15.24" y2="71.12" width="0.1524" layer="91"/>
<label x="10.16" y="68.58" size="1.778" layer="95"/>
</segment>
</net>
<net name="V-" class="0">
<segment>
<pinref part="V_SOURCE" gate="A" pin="3"/>
<wire x1="2.54" y1="91.44" x2="15.24" y2="91.44" width="0.1524" layer="91"/>
<label x="10.16" y="91.44" size="1.778" layer="95"/>
<label x="10.16" y="91.44" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$1" gate="G$1" pin="P$8"/>
<wire x1="73.66" y1="26.67" x2="83.82" y2="26.67" width="0.1524" layer="91"/>
<wire x1="83.82" y1="26.67" x2="83.82" y2="22.86" width="0.1524" layer="91"/>
<pinref part="U$2" gate="G$1" pin="P$1"/>
<wire x1="83.82" y1="22.86" x2="86.36" y2="20.32" width="0.1524" layer="91"/>
<wire x1="86.36" y1="20.32" x2="88.9" y2="20.32" width="0.1524" layer="91"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
<compatibility>
<note version="8.2" severity="warning">
Since Version 8.2, EAGLE supports online libraries. The ids
of those online libraries will not be understood (or retained)
with this version.
</note>
<note version="8.3" severity="warning">
Since Version 8.3, EAGLE supports URNs for individual library
assets (packages, symbols, and devices). The URNs of those assets
will not be understood (or retained) with this version.
</note>
</compatibility>
</eagle>
