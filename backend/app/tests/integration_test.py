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
        print(combat_container.kandinsky_supplier.generate("Sun in sky"))

    def test_kandinsky_generate_and_wait_ok(self, combat_container: Container):
        print(combat_container.kandinsky_supplier.generate_and_wait("Sun in sky"))

    def test_kandinsky_save_ok(self, combat_container: Container):
        imgs = combat_container.kandinsky_supplier.generate_and_wait(
            "Аниме девочка с флагом и медведем"
        )
        for idx, img in enumerate(imgs):
            combat_container.kandinsky_supplier.save(img, f"data/tests/{idx}.png")
