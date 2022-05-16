import { Stack } from "@mui/material";
import Head from "next/head";
import { useState } from "react";
import DurationSelector from "../src/components/DurationSelector";
import ErrorMessage from "../src/components/ErrorMessage";
import HotelroomSelector from "../src/components/HotelroomSelector";
import PrintingNotice from "../src/components/PrintingNotice";
import Ticket from "../src/components/Ticket";
import styles from "../styles/Home.module.css";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ClearIcon from '@mui/icons-material/Clear';

export default function Home() {
  const [selectedRoom, setSelectedRoom] = useState(0);
  const [duration, setDuration] = useState(0);
  const [stageIndex, setStageIndex] = useState(0);
  const [fetchError, setFetchError] = useState("");
  const [printingError, setPrintingError] = useState("");
  const [vouchers, setVouchers] = useState([]);

  const handleRoomChange = (value) => {
    setSelectedRoom(value);
    setStageIndex(1);
  };

  const handleDaysChange = (value) => {
    setDuration(value);
    setStageIndex(2);
    submitVoucherRequest(selectedRoom, value);
  };

  let stage;
  switch (stageIndex) {
    case 0:
      stage = <HotelroomSelector deliverSelectedRoom={handleRoomChange} />;
      break;
    case 1:
      stage = <DurationSelector deliverSelectedDuration={handleDaysChange} />;
      break;
    case 2:
      stage = <PrintingNotice selectedRoom={selectedRoom} days={duration} />;
      break;
  }

  async function submitVoucherRequest(selectedRoom, duration) {
    const requestOptions = {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      }
    };
    const minutes = duration * 60 * 24;
    const response = await fetch(
      "http://192.168.3.10:5000/create-voucher?minutes=" +
      minutes +
      "&count=1&quota=3&note=" +
      selectedRoom +
      "&up=5000&down=2000",
      requestOptions
    )
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        }
        setFetchError("Something went wrong. Please check your connection.");
        return;
      })
      .then((data) => {
        return data;
      })
      .catch((error) => {
        setFetchError(error.message);
      });
    if (response) {
      setVouchers(response.vouchers);
      setPrintingError(response.error);
    }
  }

  let errorMessage;
  if (fetchError) {
    errorMessage =  <ErrorMessage error={fetchError} type="error" />;
  } else if (printingError) {
    errorMessage = <ErrorMessage error={printingError} type="info"/>;
  } else {
    errorMessage = null;
  }

  const handleReset = () => {
    setSelectedRoom(0);
    setDuration(0);
    setStageIndex(0);
    setFetchError("");
    setPrintingError("");
    setVouchers([]);
  }

  const handleBack = () => {
    setStageIndex(stageIndex - 1);
  }

  return (
    <div className={styles.container}>
      <Head>
        <title>LOB - Voucher System</title>
        <meta name="description" content="" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>Locanda Oca Bianca Voucher System</h1>
        {errorMessage}
        {stage}
        {vouchers?.length > 0
          ? vouchers.map((voucher) => {
              return (
                <div key={voucher.id}>
                  <Ticket code={voucher.code} />
                </div>
              );
            })
          : null}
        <Stack direction="row" spacing={2} style={{margin : "2rem"}}>
          {stageIndex != 0 && stageIndex != 2 ? <ArrowBackIcon fontSize="large" color="primary" onClick={() => handleBack()} /> : null}
          {stageIndex != 0 ? <ClearIcon fontSize="large" color="warning" onClick={() => handleReset() } /> : null}
        </Stack>
      </main>
    </div>
  );
}
