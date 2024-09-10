import { Box } from "@chakra-ui/react";
import { SearchContext } from "context/Search";
import GetHotels from "postAPI/recipes/GetAll";
import React, { useContext } from "react";
import RecipeMap from "../../../components/RecipeMap/RecipeMap";

interface AllRecipesProps {}

const AllHotelsPage: React.FC<AllRecipesProps> = (props) => {
  const searchContext = useContext(SearchContext);

  if (localStorage.getItem("token") == null) {
    window.location.href = "/authorize";
    return (<Box></Box>);
  }

  return (
    <Box width='50%'>
      <RecipeMap searchQuery={searchContext.query} getCall={GetHotels}/>
    </Box>
  );
};

export default AllHotelsPage;
