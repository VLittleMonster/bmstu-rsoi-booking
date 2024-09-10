import React from "react";
import {
    InputProps as IProps,
    Box, Text, HStack
} from "@chakra-ui/react";
import StarIcon from "components/Icons/Star";

//import styles from "./StarBox.module.scss";

interface InputProps extends IProps {
    duration?: number
}

const StarBox: React.FC<InputProps> = (props) => {
    var stringDuration = ""

    if (!props.duration)
        stringDuration = "---"
    else
        stringDuration += props.duration

    return (
    <HStack p='2'> 
        <StarIcon /> <Text fontFamily='Bahnschrift SemiBold' color='teal' fontSize='25'> {stringDuration} </Text>
    </HStack>
    )
}

export default StarBox;