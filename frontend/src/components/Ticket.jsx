import React from "react";
import styles from "../../styles/Home.module.css";

const Ticket = (props) => {
  return (
    <>
      <p className={styles.card} style={{"fontSize" : "25pt", "letterSpacing" : "2pt"}}>{props.code}</p>
    </>
  );
};

export default Ticket;
