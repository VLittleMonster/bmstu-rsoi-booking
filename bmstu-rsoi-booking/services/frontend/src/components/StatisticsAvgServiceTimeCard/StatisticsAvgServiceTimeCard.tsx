import { Box, Text, VStack, Container, HStack, Center } from "@chakra-ui/react";
import React from "react";
import { AvgServiceTime as AvgServiceTimeI } from "types/AvgServiceTime";

//import styles from "./StatisticsAvgServiceTimeCard.module.scss";


interface StatisticsAvgServiceTimeProps extends AvgServiceTimeI {}


const StatisticsAvgServiceTimeCard: React.FC<StatisticsAvgServiceTimeProps> = (props) => {
    return (
        <Box>
            <Center>
            <Box py='2' mb='4' bg='#40E0D0' borderRadius='15' width='95%'>
                <Container>
                    <Text fontSize='xl' as='i'>{props.serviceName}</Text>
                
                    <HStack>
                    <Text color='gray.500' mr='47'>Количество запросов:</Text>
                    <Text>{props.num}</Text>
                    </HStack>
                    
                    <HStack>
                    <Text color='gray.500'>Среднее время обработки:</Text>
                    <Text>{props.avgTime.toFixed(3)} мс</Text>
                    </HStack>                
                
                </Container>
            </Box>
            </Center>
        </Box>
    )
};

export default StatisticsAvgServiceTimeCard;