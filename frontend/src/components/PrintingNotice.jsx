import React from "react";

const PrintingNotice = (props) => {
  return (
    <>
      <p style={{ fontSize: "1.25rem", margin: 0, lineHeight: 1.5 }}>
        Printing Voucher for room {props.selectedRoom}, valid for {props.days}{" "}
        Days.
      </p>
    </>
  );
};

export default PrintingNotice;
