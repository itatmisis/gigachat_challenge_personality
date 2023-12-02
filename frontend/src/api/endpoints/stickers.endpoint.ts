import { StickerReq } from "api/models/sticker.model";
import axios from "axios";

axios.defaults.baseURL = "https://kodiki-hack.ru:8000/";

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

export const fetchImage = async (id: string) => {
  const res = await axios.get(`/images/${id}`, { responseType: "blob" });
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      resolve(reader.result);
    };
    reader.onerror = reject;
    reader.readAsDataURL(res.data);
  });
};
