import React from "react";
import styles from '../../styles/Home.module.css';

export default function HotelroomsSelector(props) {

        const hotelrooms = [[100, 101, 102, 103, 104, 105, 106], [200, 201, 202, 203, 204, 205], [300, 301, 302, 303, 304, 305, 306]]

        const handleRoomChange = (value) => {
            console.log(props);
            props.deliverSelectedRoom(value);
        }
        return (
            <>{
                hotelrooms.map((floor) => (
                    <div key={floor} className={styles.grid}>
                        {
                            floor.map((room) => (
                                <h2 className={styles.card}
                                    key={room}
                                    onClick={() => handleRoomChange(room)}>
                                    {room}
                                </h2>
                            ))
                        }
                    </div>
                ))
            }</>
        );
    }
