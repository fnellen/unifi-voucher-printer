import React from "react";
import styles from "../../styles/Home.module.css";

export default function HotelroomSelector(props) {
  const hotelrooms = [
    [1, 2, 3, 4, 5],
    [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
    [201, 202, 203],
  ];

  const handleRoomChange = (value) => {
    props.deliverSelectedRoom(value);
  };
  return (
    <>
      <div className="container">
        <h2>Select the hotel room</h2>
      </div>
      {hotelrooms.map((floor) => (
        <div key={floor} className={styles.grid}>
          {floor.map((room) => (
            <h2
              className={styles.card}
              key={room}
              onClick={() => handleRoomChange(room)}
            >
              {room}
            </h2>
          ))}
        </div>
      ))}
    </>
  );
}
