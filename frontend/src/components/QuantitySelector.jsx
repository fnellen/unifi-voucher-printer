import React from "react";
import styles from "../../styles/Home.module.css";
import { IconButton, TextField } from "@mui/material";
import { useState } from "react";
import ArrowRightAltIcon from "@mui/icons-material/ArrowRightAlt";

const QuantitySelector = (props) => {
  const quantity = [1, 2, 3, 4, 5];

  const [error, setError] = useState(false);
  const [errorText, setErrorText] = useState("");
  const [customQuantity, setCustomQuantity] = useState("");

  const handleQuantityChange = (value) => {
    props.deliverSelectedQuantity(value);
  };

  const handleCustomQuantity = () => {
    if (customQuantity > 5 && customQuantity < 11 && customQuantity != null) {
      props.deliverSelectedQuantity(customQuantity);
    } else {
      setError(true);
      setErrorText("Input not in rage 6 - 10");
    }
  };
  return (
    <>
      <div className={styles.container}>
        <h2>Select the quantity of persons</h2>
      </div>
      <div className={styles.grid}>
        {quantity.map((day) => (
          <h2
            className={styles.card}
            key={day}
            onClick={() => handleQuantityChange(day)}
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
            onChange={(event) => setCustomQuantity(event.target.value)}
            InputProps={{
              endAdornment: (
                <IconButton onClick={() => handleCustomQuantity()}>
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

export default QuantitySelector;
