import { observer } from "mobx-react-lite";
import { useState } from "react";
import { LandingPageViewModel } from "./landing.vm";

export const LandingPage = observer(() => {
  const [vm] = useState(() => new LandingPageViewModel());
  return <>LandingPage</>;
});
