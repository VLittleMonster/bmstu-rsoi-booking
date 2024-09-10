import React from "react";
import {
  Text,
  Box,
  Center,
} from "@chakra-ui/react";

//import styles from "./Titles.module.scss";


export interface TitlesProps {
  subtitle?: string
  title: string
  undertitle?: string
}

const Titles: React.FC<TitlesProps> = (props) => {
  return (
    <Box fontFamily='Century Gothic' fontSize='xl' as='b'>
      <Center>
        <Text id="undertitle">
            {props.undertitle ? props.undertitle : "ㅤ"}
        </Text>
      </Center>
    </Box>
  );
};

export default React.memo(Titles);
