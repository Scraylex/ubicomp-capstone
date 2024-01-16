const EVENT_SIZE = 24;
const address = NRF.getAddress();

NRF.setServices({
  'BCDE': { // Service UUID
    'ABCD': { // Characteristic UUID
      maxLen : EVENT_SIZE,
      broadcast : false,
      readable : true,
      writable : false,
      notify : true,
      description: address
    }
  }
});

Puck.on('accel', function(d) {
  const buffer = new DataView(new ArrayBuffer(EVENT_SIZE));
  buffer.setInt32(0,d.gyro.x, true);
  buffer.setInt32(4,d.gyro.y, true);
  buffer.setInt32(8,d.gyro.z, true);
  buffer.setInt32(12,d.acc.x, true);
  buffer.setInt32(16,d.acc.y, true);
  buffer.setInt32(20,d.acc.z, true);
  const byteArray = new Uint8Array(buffer.buffer);
  NRF.updateServices({
    0xBCDE: { // Service UUID
      0xABCD: { // Characteristic UUID
        value : byteArray.buffer,
        maxLen : EVENT_SIZE,
        broadcast : false,
        readable : true,
        writable : false,
        notify : true,
        description: address
      }
    }
  });
});

Puck.accelOn(12.5);