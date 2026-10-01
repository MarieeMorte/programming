import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation


def animate_buffon_full(l=0.8, d=1.0, n_total=500, fps=20, save_path=None, seed=None):
    rng = np.random.default_rng(seed)

    x_all = rng.uniform(low=0.0, high=float(d) / 2.0, size=int(n_total))
    phi_all = rng.uniform(low=0.0, high=float(np.pi) / 2.0, size=int(n_total))
    crossed_all = x_all <= (l / 2.0) * np.sin(phi_all)

    length = 10 * d
    height = 5 * d
    cx_all = rng.uniform(low=0.0, high=float(length), size=int(n_total))
    k_line_all = rng.integers(0, 5, n_total)
    side_all = rng.integers(0, 2, n_total)
    cy_all = k_line_all * d + np.where(side_all == 1, x_all, d - x_all)

    n_arr = np.arange(1, n_total + 1)
    p_hat = np.cumsum(crossed_all) / n_arr
    p_safe = np.where(p_hat > 0, p_hat, np.nan)
    pi_hat = 2.0 * l / (p_safe * d)

    p_theor = 2 * l / (np.pi * d)

    fig = plt.figure(figsize=(15, 7.5))
    gs = gridspec.GridSpec(
        3, 2, figure=fig,
        width_ratios=[1.15, 1.0],
        height_ratios=[2.4, 2.4, 1.0],
        hspace=0.55, wspace=0.22
    )
    ax_left = fig.add_subplot(gs[0:2, 0])
    ax_info = fig.add_subplot(gs[2, 0])
    ax_p = fig.add_subplot(gs[0, 1])
    ax_pi = fig.add_subplot(gs[1, 1])

    for k in range(6):
        ax_left.axhline(k * d, color='black', lw=1)
    ax_left.set_xlim(0, length)
    ax_left.set_ylim(0, height)
    ax_left.set_aspect('equal')
    ax_left.set_title(f'Бросаем иглы  (l = {l}, d = {d})')
    ax_left.set_xlabel('x')
    ax_left.set_ylabel('y')

    ax_info.axis('off')
    info = ax_info.text(
        0.0, 0.95, '', transform=ax_info.transAxes,
        va='top', ha='left', fontsize=12, family='monospace',
        bbox=dict(boxstyle='round', fc='#f7f7f7', ec='gray', alpha=0.95)
    )

    ax_p.axhline(p_theor, color='red', ls='--', lw=1.6,
                 label=f'теория: {p_theor:.4f}')
    line_p, = ax_p.plot([], [], color='steelblue', lw=1.8,
                        label=r'оценка $P$')
    ax_p.set_xlim(0, n_total)
    ax_p.set_ylim(0, 1)
    ax_p.set_xlabel('Число бросков')
    ax_p.set_ylabel(r'$P$')
    ax_p.set_title(r'Сходимость $P$ к $\frac{2l}{\pi d}$')
    ax_p.legend(loc='upper right', fontsize=9)
    ax_p.grid(True, alpha=0.3)

    ax_pi.axhline(np.pi, color='red', ls='--', lw=1.6,
                  label=f'настоящее π = {np.pi:.4f}')
    line_pi, = ax_pi.plot([], [], color='seagreen', lw=1.8,
                          label=r'оценка $\pi$')
    ax_pi.set_xlim(0, n_total)
    ax_pi.set_ylim(2.5, 4.0)
    ax_pi.set_xlabel('Число бросков')
    ax_pi.set_ylabel(r'$\pi$')
    ax_pi.set_title(r'Сходимость $\pi = \frac{2l}{Pd}$')
    ax_pi.legend(loc='upper right', fontsize=9)
    ax_pi.grid(True, alpha=0.3)

    fig.suptitle('Задача Бюффона: P и π из одного эксперимента',
                 fontsize=13, y=0.995)

    state = {
        'n_crossed': 0,
        'current': -1,
        'paused': False,
        'needles': [],
    }

    def draw_frame(i):
        ang = phi_all[i]
        dx = (l / 2) * np.cos(ang)
        dy = (l / 2) * np.sin(ang)
        color = 'crimson' if crossed_all[i] else 'steelblue'

        ln, = ax_left.plot(
            [cx_all[i] - dx, cx_all[i] + dx],
            [cy_all[i] - dy, cy_all[i] + dy],
            color=color, lw=1.8, alpha=0.85, solid_capstyle='round'
        )
        state['needles'].append(ln)

        if crossed_all[i]:
            state['n_crossed'] += 1

        info.set_text(
            f'Брошено:      {i + 1}\n'
            f'Пересечений:  {state["n_crossed"]}\n'
            f'Оценка P:     {p_hat[i]:.4f}\n'
            f'Оценка π:     {pi_hat[i]:.4f}'
        )

        idx = np.arange(1, i + 2)
        line_p.set_data(idx, p_hat[:i + 1])
        line_pi.set_data(idx, pi_hat[:i + 1])

    def update(frame):
        if state['paused']:
            return line_p, line_pi, info

        i = frame
        if i <= state['current']:
            for ln in state['needles']:
                ln.remove()
            state['needles'].clear()
            state['n_crossed'] = 0
            state['current'] = -1

        draw_frame(i)
        state['current'] = i
        return line_p, line_pi, info

    animation = FuncAnimation(
        fig, update,
        frames=n_total,
        interval=1000 / fps,
        blit=False,
        repeat=False,
        cache_frame_data=False
    )

    def on_key(event):
        if event.key == ' ':
            if state['paused']:
                animation.event_source.start()
                state['paused'] = False
            else:
                animation.event_source.stop()
                state['paused'] = True
            fig.canvas.draw_idle()
        elif event.key in ('r', 'R', 'к', 'К'):
            for ln in state['needles']:
                ln.remove()
            state['needles'].clear()
            state['n_crossed'] = 0
            state['current'] = -1
            state['paused'] = False
            info.set_text('')
            ax_info.set_title('')
            line_p.set_data([], [])
            line_pi.set_data([], [])
            animation.frame_seq = animation.new_frame_seq()
            animation.event_source.start()
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect('key_press_event', on_key)

    if save_path:
        animation.save(save_path, fps=fps, dpi=110)
        print(f'Анимация сохранена: {save_path}')

    return animation


if __name__ == '__main__':
    anim = animate_buffon_full(l=0.8, d=1.0, n_total=500, fps=20)
    plt.show()
