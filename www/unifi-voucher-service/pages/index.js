import Head from "next/head";
import { useState } from "react";
import DurationSelector from "../src/components/DurationSelector";
import HotelroomSelector from "../src/components/HotelroomSelector";
import PrintingNotice from "../src/components/PrintingNotice";
import styles from "../styles/Home.module.css";

export default function Home() {
  const [selectedRoom, setSelectedRoom] = useState(0);
  const [duration, setDuration] = useState(0);
  const [stageIndex, setStageIndex] = useState(0);
  const [vouchers, setVouchers] = useState([
    {
      "adminName": "",
      "code": "",
      "creationTime": 0,
      "duration": 0,
      "id": "",
      "note": "",
      "siteId": "",
      "speedDown": "",
      "speedUp": "",
      "status": "",
      "statusExpires": 0,
      "usageQuota": 0,
      "used": 0
    }
  ]);

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
      stage = <PrintingNotice selectedRoom={selectedRoom} days={duration}/>;
      break;
  }

  async function submitVoucherRequest(selectedRoom, duration) {
    const requestOptions = {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
        "access-control-allow-origin": "localhost:3000",
      },
      //agent: httpsAgent,
    };
    const minutes = duration * 60 * 24;
    const response = await fetch("http://localhost:5001/create-voucher?minutes="+ minutes +"&count=1&quota=3&note="+selectedRoom+"&up=5000&down=2000", requestOptions)
      .then((response) => {
        if (response.status === 200) {
          return response.json()
        }
        return Error("Error: " + response.status);
      }
      )
      .then((data) => {
        return data.vouchers;
      })
      .catch((error) => {
        throw new Error("Error: " + error);
      });
    setVouchers(response);
  }

  return (
    <div className={styles.container}>
      <Head>
        <title>LOC - Voucher System</title>
        <meta name="description" content="" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>Locanda Oca Bianca Voucher System</h1>
        {stage}
        {vouchers.map((voucher) => {
          return (
            <div key={voucher.id}>
              <h2>Voucher code for room {voucher.code}</h2>
            </div>
          );
        })
        }
      </main>
    </div>
  );
}
