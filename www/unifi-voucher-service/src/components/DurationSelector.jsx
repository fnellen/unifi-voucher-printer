import React from "react";
import styles from "../../styles/Home.module.css";
import { IconButton, TextField } from "@mui/material";
import { useState } from "react";
import ArrowRightAltIcon from "@mui/icons-material/ArrowRightAlt";

const DurationSelector = (props) => {
  const duration = [1, 2, 3, 4, 5];

  const [error, setError] = useState(false);
  const [errorText, setErrorText] = useState("");
  const [customDuration, setCustomDuration] = useState("");

  const handleDurationChange = (value) => {
    props.deliverSelectedDuration(value);
  };

  const handleCustomDuration = () => {
    if (customDuration > 5 && customDuration < 30 && customDuration != null) {
      props.deliverSelectedDuration(customDuration);
    } else {
      setError(true);
      setErrorText("Input not in rage 5 - 100");
    }
  };
  return (
    <>
      <div className="container">
        <h2>Select the duration</h2>
      </div>
      <div className={styles.grid}>
        {duration.map((day) => (
          <h2
            className={styles.card}
            key={day}
            onClick={() => handleDurationChange(day)}
          >
            {day}
          </h2>
        ))}
        <div className="styles.card">
          <TextField
            sx={{
              margin: "1rem",
              padding: "1.5rem",
              textAlign: "center",
              color: "inherit",
              textDecoration: "none",
              size: "small",
              border: "1px solid #eaeaea",
              borderRadius: "10px",
              transition: "color 0.15s ease, border-color 0.15s ease",
            }}
            error={error}
            helperText={errorText}
            type="number"
            onChange={(event) => setCustomDuration(event.target.value)}
            InputProps={{
              endAdornment: (
                <IconButton onClick={() => handleCustomDuration()}>
                  <ArrowRightAltIcon />
                </IconButton>
              ),
            }}
          ></TextField>
        </div>
      </div>
    </>
  );
};

export default DurationSelector;
