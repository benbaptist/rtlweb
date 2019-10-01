class Demods:
    def __init__(self, radio, mode):
        self.radio = radio
        self.mode = mode
        self.log = radio.log_manager.getLogger("Radio/%s" % self.mode)

        self.current_freq = radio.freq

    # def realtick(self):
    #     self.tick()

    def tick(self):
        self.log.warning("Unimplemented (tick)")

    def shutdown(self):
        self.log.warning("Unimplemented (shutdown)")
