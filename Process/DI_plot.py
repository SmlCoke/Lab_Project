"""Compute post-implant diffusion profiles for a single implant."""

import argparse
import math
from typing import Iterable, List, Optional, Tuple

import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError:  # matplotlib may be missing on some exam machines
    plt = None


def gaussian_profile(x_cm: np.ndarray, dose: float, rp_cm: float, sigma_cm: float) -> np.ndarray:
    coeff = dose / (math.sqrt(2 * math.pi) * sigma_cm)
    return coeff * np.exp(-((x_cm - rp_cm) ** 2) / (2 * sigma_cm**2))


def diffused_profile(
    x_cm: np.ndarray, dose: float, rp_cm: float, sigma_cm: float, diffusivity: float, t_s: float
) -> Tuple[np.ndarray, float]:
    sigma_eff = math.sqrt(sigma_cm**2 + 2 * diffusivity * t_s)
    return gaussian_profile(x_cm, dose, rp_cm, sigma_eff), sigma_eff


def junction_depth_cm(
    dose: float, rp_cm: float, sigma_cm: float, diffusivity: float, t_s: float, background: float
) -> Tuple[Optional[float], float, float]:
    sigma_eff = math.sqrt(sigma_cm**2 + 2 * diffusivity * t_s)
    peak = dose / (math.sqrt(2 * math.pi) * sigma_eff)
    ratio = background * math.sqrt(2 * math.pi) * sigma_eff / dose
    if ratio <= 0 or ratio >= 1:
        return None, sigma_eff, peak
    delta = math.sqrt(-2 * sigma_eff**2 * math.log(ratio))
    return rp_cm + delta, sigma_eff, peak


def build_depth_grid(depth_um: float, points: int) -> np.ndarray:
    depth_cm = depth_um * 1e-4
    return np.linspace(0, depth_cm, points)


def summarize_results(
    times_hr: Iterable[float],
    junctions_cm: List[Optional[float]],
    sigmas_cm: List[float],
    peaks: List[float],
    target_depth_um: float,
):
    header = (
        "Time(h)   sigma_eff(um)   peak(cm^-3)        xj(um)       reaches {:.2f}um".format(
            target_depth_um
        )
    )
    print(header)
    print("-" * len(header))
    for t, xj, sigma, peak in zip(times_hr, junctions_cm, sigmas_cm, peaks):
        xj_um = "--" if xj is None else f"{xj * 1e4:8.3f}"
        hit = "No" if xj is None else ("Yes" if xj * 1e4 >= target_depth_um else "No")
        print(f"{t:6.2f}   {sigma * 1e4:12.4f}   {peak:12.3e}   {xj_um:>8}   {hit:>6}")


def plot_profiles(
    x_cm: np.ndarray,
    baseline: np.ndarray,
    profiles: List[np.ndarray],
    times_hr: Iterable[float],
    background: float,
    target_depth_um: float,
):
    if plt is None:
        print("matplotlib is not available; skipping plot.")
        return
    x_um = x_cm * 1e4
    plt.figure(figsize=(7, 5))
    plt.semilogy(x_um, baseline, label="As-implanted")
    for profile, t in zip(profiles, times_hr):
        plt.semilogy(x_um, profile, label=f"t = {t:.0f} h")
    plt.axhline(background, color="k", linestyle="--", linewidth=1, label="Background")
    plt.axvline(target_depth_um, color="gray", linestyle=":", linewidth=1, label="Target depth")
    plt.xlabel("Depth (um)")
    plt.ylabel("Concentration (cm^-3)")
    plt.title("Phosphorus profile after drive-in")
    plt.grid(True, which="both", linestyle=":", linewidth=0.8)
    plt.legend()
    plt.tight_layout()
    plt.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fast solver for implanted Gaussian + drive-in diffusion",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--dose", type=float, default=1e18, help="Implant dose (atoms/cm^2)")
    parser.add_argument("--rp-nm", type=float, default=50.0, help="Projected range Rp (nm)")
    parser.add_argument("--sigma-nm", type=float, default=20.0, help="Standard deviation ΔRp (nm)")
    parser.add_argument("--diffusivity", type=float, default=1e-13, help="Diffusivity D (cm^2/s)")
    parser.add_argument(
        "--times", type=str, default="1,3,5", help="Comma-separated drive-in times (hours)"
    )
    parser.add_argument("--background", type=float, default=1e16, help="Substrate concentration (cm^-3)")
    parser.add_argument("--depth-um", type=float, default=3.0, help="Plot depth window (um)")
    parser.add_argument("--points", type=int, default=500, help="Number of grid points")
    parser.add_argument("--no-plot", action="store_true", help="Do not display profile plot")
    return parser.parse_args()


def main():
    args = parse_args()
    times_hr = [float(t.strip()) for t in args.times.split(",") if t.strip()]
    x_cm = build_depth_grid(args.depth_um, args.points)
    rp_cm = args.rp_nm * 1e-7
    sigma_cm = args.sigma_nm * 1e-7
    baseline = gaussian_profile(x_cm, args.dose, rp_cm, sigma_cm)

    profiles: List[np.ndarray] = []
    junctions: List[Optional[float]] = []
    sigmas: List[float] = []
    peaks: List[float] = []

    for t_hr in times_hr:
        profile, sigma_eff = diffused_profile(
            x_cm, args.dose, rp_cm, sigma_cm, args.diffusivity, t_hr * 3600
        )
        xj, sigma_final, peak = junction_depth_cm(
            args.dose, rp_cm, sigma_cm, args.diffusivity, t_hr * 3600, args.background
        )
        profiles.append(profile)
        junctions.append(xj)
        sigmas.append(sigma_final)
        peaks.append(peak)

    summarize_results(times_hr, junctions, sigmas, peaks, args.depth_um)

    if not args.no_plot:
        plot_profiles(x_cm, baseline, profiles, times_hr, args.background, args.depth_um)


if __name__ == "__main__":
    main()
