# Roomba Enhanced Integration

An enhanced Home Assistant integration for iRobot Roomba vacuums, built on top of the official integration with additional features.

## Features

✅ **All Official Features**: Compatible with the official HA Roomba integration  
✅ **Enhanced Room Cleaning**: Clean specific rooms or multiple rooms  
✅ **Advanced Mapping**: Real-time position tracking and room detection  
✅ **Enhanced Sensors**: Detailed position, mission, and status sensors  
✅ **Map Visualization**: Camera entity for map display (coming soon)  
✅ **Custom Services**: Dedicated services for room-based cleaning  

## Installation

1. Copy the `roomba_enhanced` folder to your `custom_components` directory
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration
4. Search for "iRobot Roomba Enhanced"
5. Enter your Roomba's IP address, BLID, and password

## Getting Credentials

You can obtain your Roomba's credentials using:

- **roombapy discovery tool**:
  ```bash
  roombapy discover <roomba_ip>
  ```

- **dorita980 password tool**:
  ```bash
  npm install -g dorita980
  get-roomba-password-cloud <email> <password>
  ```

## Enhanced Services

### Clean Room
Clean a specific room by ID:
```yaml
service: roomba_enhanced.clean_room
data:
  entity_id: vacuum.roomba_enhanced
  room_id: "1"
```

### Clean Multiple Rooms
Clean multiple rooms (ordered or simultaneous):
```yaml
service: roomba_enhanced.clean_rooms
data:
  entity_id: vacuum.roomba_enhanced
  room_ids: ["1", "3", "5"]
  ordered: true
```

## Enhanced Entities

### Vacuum Entity
- All standard vacuum features
- Enhanced room cleaning via `send_command`
- Detailed state attributes including available rooms

### Sensors
- **Battery**: Battery percentage with charging status
- **Bin Full**: Bin status with presence detection
- **Phase**: Current cleaning phase
- **Mission Time**: Duration of current/last mission
- **Position X/Y**: Real-time robot coordinates

### Camera Entity
- Map visualization (placeholder - coming soon)
- Room layout and robot position display

## Integration with Existing Cards

Works with popular vacuum cards:

### Xiaomi Vacuum Card
```yaml
type: custom:xiaomi-vacuum-card
entity: vacuum.roomba_enhanced
```

### Vacuum Card
```yaml
type: custom:vacuum-card
entity: vacuum.roomba_enhanced
shortcuts:
  - name: Clean Kitchen
    service: roomba_enhanced.clean_room
    service_data:
      entity_id: vacuum.roomba_enhanced
      room_id: "1"
```

## Why This Integration?

This integration enhances the official Roomba integration by:

1. **Building on proven foundation**: Uses the same roombapy library as the official integration
2. **Adding advanced features**: Room cleaning, enhanced mapping, detailed sensors
3. **Maintaining compatibility**: Works alongside or replaces the official integration
4. **Providing flexibility**: Enhanced services and configuration options

## Credits

Built on top of:
- [Official Home Assistant Roomba Integration](https://github.com/home-assistant/core/tree/dev/homeassistant/components/roomba)
- [roombapy](https://github.com/pschmitt/roombapy) by @pschmitt
- [dorita980](https://github.com/koalazak/dorita980) for inspiration

## Future Enhancements

- [ ] Visual map generation with PIL/Pillow
- [ ] Zone cleaning capabilities  
- [ ] Schedule management
- [ ] Multi-floor map support
- [ ] Integration with vacuum cards for room selection UI 