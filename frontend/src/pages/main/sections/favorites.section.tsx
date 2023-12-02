import { FCVM } from '@/utils/fcvm';
import { observer } from 'mobx-react-lite';
import { MainPageViewModel } from '../../main.vm';

export const FavoritesSection: FCVM<MainPageViewModel> = observer(({ vm }) => {
  return (
    <>
       FavoritesSection
    </>
  );
});