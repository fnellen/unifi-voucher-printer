import Head from 'next/head'
import { useState } from 'react'
import DurationSelector from '../src/components/DurationSelector'
import HotelroomsSelector from '../src/components/HotelroomsSelector'
import styles from '../styles/Home.module.css'

export default function Home() {

  const [selectedRoom, setSelectedRoom] = useState(0)
  const [days, setDays] = useState(0)
  const [stageIndex, setStageIndex] = useState(0)

  const hotelrooms = [[100, 101, 102, 103, 104, 105, 106], [200, 201, 202, 203, 204, 205], [300, 301, 302, 303, 304, 305, 306]]

  const handleRoomChange = (value) => {
    setSelectedRoom(value);
    console.log(selectedRoom);
    setStageIndex(1);
  }

  const handleDaysChange = (value) => {
    setDays(value);
    console.log(days);
  }
  let stage;
  if (stageIndex === 0) {
    stage = <HotelroomsSelector deliverSelectedRoom={() => handleRoomChange()}/>
  } else if (stageIndex === 1) {
    stage = <DurationSelector deliverSelectedDuration={() => handleDaysChange()} />
  }

  return (
    <div className={styles.container}>
      <Head>
        <title>LOC - Voucher System</title>
        <meta name="description" content="" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Locanda Oca Bianca Voucher System
        </h1>

        <div className="container">
          <h2>Select the hotel room</h2>
        </div>

        {stage}
      </main>
    </div>
  )
}
