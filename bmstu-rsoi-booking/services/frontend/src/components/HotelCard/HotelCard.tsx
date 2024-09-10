import { Box, HStack, Image, Text, Badge, Center} from "@chakra-ui/react";
import React from "react";

import { Hotel as HotelI } from "types/Hotel";

import StarBox from "components/Boxes/Star";
import FullLikeBox from "components/Boxes/FullLike";

//import styles from "./HotelCard.module.scss";
import GetImageUrl from "postAPI/likes/Get";

import CalendarWidget from "components/DateInput";
import {DateReservation as DateReservationT} from "types/DateReservation";
import {ReservationRequest as ReservationRequestT} from "types/ReservationRequest";
import PostReservation from "postAPI/likes/Post";


interface HotelProps extends HotelI {}

const HotelCard: React.FC<HotelProps> = (props) => {
  const [imageUrl, setImageUrl] = React.useState("https://media.discordapp.net/attachments/791290400086032437/1112498073478889502/default-fallback-image.png?width=720&height=480");

  async function getImageUrl() {
    var data = await GetImageUrl(props.hotelUid);
    if (data.status === 200) {
      setImageUrl(data.content);
    }
  }

  async function putDateReservation(dataInfo: DateReservationT) {
    const reservationRequest: ReservationRequestT = { 
      hotelUid: props.hotelUid, 
      startDate: dataInfo.startDate.toLocaleDateString("en-CA"),
      endDate: dataInfo.endDate.toLocaleDateString("en-CA") 
    };

    await PostReservation(reservationRequest);
  }

  getImageUrl();

  return (
    <Box mb='5' bg='#40E0D0' p='3' borderRadius='15' borderWidth='1px'>

      <Box p='3' borderWidth='1px' borderColor='#008080' borderRadius='10'>
      <Image src='https://cdn1.img.sputniknews.uz/img/07e7/02/02/31925909_0:160:3073:1888_640x0_80_0_0_fd551a1f7d7e4ffc3b470903a63de07d.jpg' 
      borderRadius='15'>
      </Image>
          <Badge mt='2' fontFamily='Agency FB' borderRadius='full' px='65' colorScheme='teal' fontSize='3xl' width='100%'>
            <Center>{props.name}</Center>
          </Badge>
          
          <Center>
          <HStack>
            <Text fontFamily='Century Gothic'>{props.country}</Text>
            <Text as='u' color='gray.600' fontFamily='Century Gothic'>{props.city}</Text>
            <Text as='u' color='gray.600' fontFamily='Century Gothic'>{props.address}</Text>
          </HStack>
          </Center>

        <Center>
        <HStack>
          <StarBox duration={props.stars} />
          <FullLikeBox price={props.price} />
        </HStack>
        </Center>

        <CalendarWidget putCallback={(data: DateReservationT) => putDateReservation(data)}/>

      </Box>
    </Box>
  );
};

export default HotelCard;
