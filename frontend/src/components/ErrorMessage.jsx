import React from "react";
import styles from "../../styles/Home.module.css";

const ErrorMessage = (props) => {

    let styleName;

    if (props.type == "error") {
        styleName = styles.errorCard;
    } else if (props.type == "info") {
        styleName = styles.infoCard;
    }

    return (
        <>
            <div className={styleName} >
                <h2>{props.error}</h2>
            </div>
        </>
  );
};

export default ErrorMessage;
