import { Box, Button, Center, useDisclosure } from '@chakra-ui/react'
import { useState } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
} from '@chakra-ui/react'
import React from 'react'

import { DateReservation as DateReservationT } from 'types/DateReservation';

import DateInputBox from 'components/DateInputBox/DateInputBox'


interface DateContextType {
  startDate: string,
  setStartDate: React.Dispatch<React.SetStateAction<string>>,
  endDate: string,
  setEndDate: React.Dispatch<React.SetStateAction<string>>
}

export const DateContext = React.createContext<DateContextType | undefined>(undefined);


export default function DateInput(props) {
  const { isOpen, onOpen, onClose } = useDisclosure()
  const [ startDate, setStartDate] = useState('');
  const [ endDate, setEndDate] = useState('');

  var data: DateReservationT = { startDate: new Date(), endDate: new Date() }

  async function put() { 
    data.startDate = new Date(startDate);
    data.endDate = new Date(endDate);

    if (CheckDate(startDate) || CheckDate(endDate)){  
      // ОПОВЕСТИТЬ ЮЗЕРА, О ТОМ ЧТО ДАТЫ ВЫБРАНЫ НЕ КОРРЕКТНО (возможно выделить цветом рамки некорректных дат)
      return;
    }

    await props.putCallback(data);
    onClose();
  }

  return (
    <>
      <Button onClick={onOpen} width='100%' colorScheme='teal' fontFamily='Century Gothic' fontSize='xl'>
          Забронировать
      </Button>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader ml='55' fontSize='l' fontFamily='Century Gothic'>Выберете даты въезда и выезда</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
          <Center>
            <Box borderWidth='1px' borderColor='teal' width='50%'>
              <DateContext.Provider value={{ startDate, setStartDate, endDate, setEndDate }}>
                <DateInputBox/>
              </DateContext.Provider>
            </Box>
          </Center>

            <Button mt='3'colorScheme='teal' fontFamily='Century Gothic' width='100%' onClick={put}>
              Подтвердить бронирование
            </Button>
          </ModalBody>
          <ModalFooter/>
        </ModalContent>
      </Modal>
    </>
  )
}

function CheckDate(val: string): boolean {
  return val === null || val === undefined || val.length <= 0;
}
