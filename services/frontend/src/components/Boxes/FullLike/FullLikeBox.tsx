import React from "react";
import {
    InputProps as IProps, Text, HStack
} from "@chakra-ui/react";

interface InputProps extends IProps {
    price?: number | string
}

const FullLikeBox: React.FC<InputProps> = (props) => {
    return (
    <HStack>
        <Text fontFamily='Bahnschrift SemiBold' color='teal' fontSize='25'>(₽) {props.price} </Text>
    </HStack>
    )
}

export default FullLikeBox;