import React from "react";
import { useState } from "react";
import styles from '../../styles/Home.module.css';

const DurationSelector = (props) => {
    
        const [selectedRoom, setSelectedRoom] = useState(0)

        const duration = [1,2,3,4,5]

        const handleRoomChange = (value) => {
            props.deliverSelectedRoom(value);
        }
        return (
            <>{
                duration.map((floor) => (
                    <div key={floor} className={styles.grid}>
                        {
                            floor.map((room) => (
                                <h2 className={styles.card}
                                    key={room}
                                    onClick={() => handleRoomChange(room)}>
                                    {room}
                                </h2>
                            ))}
                    </div>
                ))
            }</>
        );
    }

export default DurationSelector;