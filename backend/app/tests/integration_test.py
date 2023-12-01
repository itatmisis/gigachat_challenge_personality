from shared.containers import Container


class TestIntegration:
    def test_get_ddl_ok(self, combat_container: Container):
        ...
        # print(combat_container.heath_service.db_repository.compile_table(ATM))
        # print(combat_container.heath_service.db_repository.compile_table(Office))

    async def test_check_ok(self, combat_container: Container):
        await combat_container.heath_service.check()

    def test_kandinsky_get_model_ok(self, combat_container: Container):
        print(combat_container.kandinsky_supplier.get_model())

    def test_kandinsky_generate_ok(self, combat_container: Container):
        print(
            combat_container.kandinsky_supplier.generate(
                "Sun in sky",
                style="ANIME",
                width=1023,
                height=1023,
                negative_prompt=None,
            )
        )

    def test_kandinsky_generate_and_wait_ok(self, combat_container: Container):
        print(combat_container.kandinsky_supplier.generate_and_wait("Sun in sky"))

    def test_kandinsky_save_ok(self, combat_container: Container):
        imgs = combat_container.kandinsky_supplier.generate_and_wait(
            "Undeaged anime sticker girl with (plush bear) in left hand and (green flag) in right hand",
            style="ANIME",
            images=3,
        )
        if imgs is None:
            return

        for idx, img in enumerate(imgs):
            combat_container.kandinsky_supplier.save(img, f"data/tests/{idx}.png")

    def test_gigachat_ok(self, combat_container: Container):
        res = combat_container.gigachat_supplier.single_message(
            "Сделай пропт для кандинского для классного аниме стикера",
        )
        print(res)
