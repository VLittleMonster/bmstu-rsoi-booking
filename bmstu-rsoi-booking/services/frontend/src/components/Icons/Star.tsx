// import theme from "styles/extendTheme";
import React from "react";
import LogoProps from "./Logo"

const StarIcon: React.FC<LogoProps> = (props) => {
    var w = props.width ? props.width: "25px";
    var h = props.height ? props.height: "25px";
    var fill = props.fill ? props.fill : 'teal';
    return (
        <svg width={w} height={h} fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fill={fill} d="M2.18005 8.24008L6.10005 12.0601L5.18005 17.4401L10.0001 14.9001L14.8201 17.4401L13.9001 12.0601L17.8201 8.24008L12.4201 7.46008L10.0001 2.58008L7.58005 7.46008L2.18005 8.24008Z"/>   
        </svg>
    );
}

export default StarIcon
