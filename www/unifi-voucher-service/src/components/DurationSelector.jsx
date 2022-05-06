import React from "react";
import styles from '../../styles/Home.module.css';

const DurationSelector = (props) => {

        const duration = [1,2,3,4,5]

        const handleDurationChange = (value) => {
            props.deliverSelectedDuration(value);
        }
        return (
            <div className={styles.grid}>
                {
                    duration.map((day) => (
                        <h2 className={styles.card}
                            key={day}
                            onClick={() => handleDurationChange(day)}>
                            {day}
                        </h2>
                    ))
                }
            </div>
        );
    }

export default DurationSelector;