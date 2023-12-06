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