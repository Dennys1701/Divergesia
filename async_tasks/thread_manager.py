
class ThreadManager:
    def __init__(self):
        self.workers = []

    def add_worker(self, worker):
        self.workers.append(worker)
        # Limpiar trabajadores finalizados periódicamente
        self.cleanup()

    def cleanup(self):
        # Eliminar referencias a threads que ya no están corriendo
        self.workers = [w for w in self.workers if w.isRunning()]

    def cancel_all(self):
        # QThread no ofrece cancelación forzada; se debe manejar lógicamente en slots
        self.workers.clear()