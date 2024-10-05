import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#Configurar la ventana
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

x_data, y_data_percent, y_data_used, y_data_available, y_data_total = [], [], [], [], []
line_percent, = ax1.plot([], [], label='Uso (%)')
line_used, = ax1.plot([], [], label='Memoria Usada (MB)')
line_available, = ax1.plot([], [], label='Memoria Disponible (MB)')
line_total, = ax1.plot([], [], label='Memoria Total (MB)', linestyle='--')

memory_total = psutil.virtual_memory().total / (1024 ** 2)  #MB

#Función para actualizar el gráfico y los procesos en tiempo real
def update(frame):
    memory_info = psutil.virtual_memory()

    memory_percent = memory_info.percent
    memory_used = memory_info.used / (1024 ** 2)  #MB
    memory_available = memory_info.available / (1024 ** 2)  #MB

    x_data.append(frame)
    y_data_percent.append(memory_percent)
    y_data_used.append(memory_used)
    y_data_available.append(memory_available)
    y_data_total.append(memory_total)

    line_percent.set_data(x_data, y_data_percent)
    line_used.set_data(x_data, y_data_used)
    line_available.set_data(x_data, y_data_available)
    line_total.set_data(x_data, y_data_total)

    ax1.relim()
    ax1.autoscale_view()

    processes = [(p.info['name'], p.info['memory_info'].rss / (1024 ** 2))
                 for p in psutil.process_iter(['name', 'memory_info'])]

    more_memory_processes = sorted(processes, key=lambda x: x[1], reverse=True)[:15]

    ax2.clear()
    ax2.set_title('Procesos Ordenados Por Uso de Memoria')
    process_info = '\n'.join([f"{name}: {memory_used:.2f} MB" for name, memory_used in more_memory_processes])
    ax2.text(0.5, 0.5, process_info, ha='center', va='center', fontsize=12, transform=ax2.transAxes)
    ax2.axis('off')

    return line_percent, line_used, line_available, line_total

ani = FuncAnimation(fig, update, interval=1000)

ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Memoria')
ax1.set_title('Monitor de Uso de Memoria en Tiempo Real')
ax1.legend(loc='upper left')
plt.tight_layout()

plt.show()