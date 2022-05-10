import React from "react";

const PrintingNotice = (props) => {
  return (
    <>
      <div className="container">
        <h2>
          Printing Voucher for room {props.selectedRoom}, which is valid for{" "}
          {props.days} Days.
        </h2>
      </div>
    </>
  );
};

export default PrintingNotice;
