function loop() {
    const accel = Puck.accel();
    const csv =`${accel.acc.x},${accel.acc.y},${accel.acc.z}`;
    NRF.setAdvertising({},
        {
            showName: false,
            manufacturer: 0x0590,
            manufacturerData: csv,
            connectable: false,
            scannable : false
        });
}

setInterval(loop, 100);

---------------------------------------------

Puck.on('accel', function(d) {
    print(`${d.gyro.x},${d.gyro.y},${d.gyro.z}`);
   });
   
Puck.accelOn(12.5);

---------------------------------------------


const EVENT_SIZE = 16;

Puck.on('accel', function(d) {
    log = new DataView(new ArrayBuffer(EVENT_SIZE));
    log.setInt32(0,Date.now()/1000);
    log.setInt32(4,d.gyro.x);
    log.setInt32(8,d.gyro.y);
    log.setInt32(12,d.gyro.z);
    var byteArray = new Uint8Array(log.buffer);
    print(byteArray)
});

Puck.accelOn(12.5);

---------------------------------------------


const EVENT_SIZE = 16;
var log = new DataView(new ArrayBuffer(EVENT_SIZE*1000));

Puck.on('accel', function(d) {
    csv = `${d.gyro.x},${d.gyro.y},${d.gyro.z}`;
    NRF.setAdvertising({},
        {
            showName: false,
            manufacturer: 0x0590,
            manufacturerData: csv,
            connectable: false,
            scannable : false
        });
});

Puck.accelOn(12.5);

---------------------------------------------

const EVENT_SIZE = 16;
var log = new DataView(new ArrayBuffer(EVENT_SIZE));


Puck.on('accel', function(d) {
    log.setInt32(0,Date.now()/1000);
    log.setInt32(4,d.gyro.x);
    log.setInt32(8,d.gyro.y);
    log.setInt32(12,d.gyro.z);
    var byteArray = new Uint8Array(log.buffer);
    const byteString = E.toString(byteArray);
    print(byteString);
});

Puck.accelOn(12.5);

---------------------------------------------

const EVENT_SIZE = 16;

function loop() {
    const log = new DataView(new ArrayBuffer(EVENT_SIZE));
    const accel = Puck.accel();
    const gyro = accel.gyro;
    log.setInt32(0,Date.now()/1000);
    log.setInt32(4,gyro.x);
    log.setInt32(8,gyro.y);
    log.setInt32(12,gyro.z);
    var byteArray = new Uint8Array(log.buffer);
    const byteString = E.toString(byteArray);
    print(gyro);
    NRF.setAdvertising({},
        {
            showName: false,
            manufacturer: 0x0590,
            manufacturerData: byteString,
            connectable: false,
            scannable : false
        });
}

Puck.accelOn(12.5);
setInterval(loop, 100);

---------------------------------------------
const EVENT_SIZE = 16;
const log = new DataView(new ArrayBuffer(EVENT_SIZE));
NRF.setServices({
  'BCDE': { // Service UUID
    'ABCD': { // Characteristic UUID
      maxLen : 16,
      broadcast : false,
      readable : true,
      writable : false,
      notify : true,
      description: "Gyro data"
    }
  }
});
Puck.on('accel', function(d) {
  log.setInt32(0,Date.now()/1000);
  log.setInt32(4,d.gyro.x);
  log.setInt32(8,d.gyro.y);
  log.setInt32(12,d.gyro.z);
  print(d.gyro);
  const byteArray = new Uint8Array(log.buffer);
  const byteString = E.toString(byteArray);
  NRF.updateServices({
    0xBCDE: { // Service UUID
      0xABCD: { // Characteristic UUID
        value : byteString,
        maxLen : 16,
        broadcast : false,
        readable : true,
        writable : false,
        notify : true,
        description: "Gyro data"
      }
    }
  });
});
Puck.accelOn(12.5);
---------------------------------------------

Puck.on('accel', function(d) {
    const csv = `${parseInt(Date.now())},${d.gyro.x},${d.gyro.y},${d.gyro.z}`;
    print(csv);
});

Puck.accelOn(12.5);

---------------------------------------------

const EVENT_SIZE = 16;
const log = new DataView(new ArrayBuffer(EVENT_SIZE));
NRF.setServices({
  'BCDE': { // Service UUID
    'ABCD': { // Characteristic UUID
      maxLen : 16,
      broadcast : false,
      readable : true,
      writable : false,
      notify : true,
      description: "Gyro data"
    }
  }
});
Puck.on('accel', function(d) {
  log.setInt32(0,Date.now()/1000, true);
  log.setInt32(4,d.gyro.x, true);
  log.setInt32(8,d.gyro.y, true);
  log.setInt32(12,d.gyro.z, true);
  const byteArray = new Uint8Array(log.buffer);
  NRF.updateServices({
    0xBCDE: { // Service UUID
      0xABCD: { // Characteristic UUID
        value : byteArray,
        maxLen : 16,
        broadcast : false,
        readable : true,
        writable : false,
        notify : true,
        description: "Gyro data"
      }
    }
  });
});
Puck.accelOn(12.5);

---------------------------------------------

const EVENT_SIZE = 12;
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

