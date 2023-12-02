import { StickerReq } from "api/models/sticker.model";
import axios from "axios";

axios.defaults.baseURL = import.meta.env.VITE_API_URL;

export const generateImage = async (req: StickerReq) => {
  const { data } = await axios.post("/images/generate", req);
  return data as {
    id: string;
    prompt: string;
  };
};

export const fetchImages = async (ids: string[]) => {
  const { data } = await axios.post("/images/wait", {
    ids: ids
  });
  return data as {
    id: string;
    img: string;
  }[];
};
