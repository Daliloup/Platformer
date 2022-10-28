<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.9" tiledversion="1.9.0" name="Spikes" tilewidth="64" tileheight="64" tilecount="5" columns="5">
 <image source="../../graphics/sprites/obstacles/spike.png" width="320" height="64"/>
 <tile id="0">
  <objectgroup draworder="index" id="2">
   <object id="1" template="spike_collision.tx" x="0" y="0"/>
  </objectgroup>
 </tile>
 <tile id="1">
  <objectgroup draworder="index" id="2">
   <object id="1" template="spike_collision.tx" x="0" y="0"/>
  </objectgroup>
 </tile>
 <tile id="2">
  <objectgroup draworder="index" id="2">
   <object id="1" template="spike_collision.tx" x="0" y="0"/>
  </objectgroup>
 </tile>
 <tile id="3">
  <objectgroup draworder="index" id="2">
   <object id="1" template="spike_collision.tx" x="0" y="0"/>
  </objectgroup>
 </tile>
 <tile id="4">
  <objectgroup draworder="index" id="3">
   <object id="4" template="spike_collision.tx" x="0" y="0" visible="1"/>
  </objectgroup>
  <animation>
   <frame tileid="0" duration="2000"/>
   <frame tileid="1" duration="75"/>
   <frame tileid="2" duration="75"/>
   <frame tileid="3" duration="75"/>
   <frame tileid="4" duration="75"/>
  </animation>
 </tile>
</tileset>
