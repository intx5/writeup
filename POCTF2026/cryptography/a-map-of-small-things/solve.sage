
p  = 17759930830448937043
Gx, Gy = 2, 2130375071143573863
Qx, Qy = 883597023359665637, 2985448497230721926

E = EllipticCurve(GF(p), [1, 0])
G, Q = E(Gx, Gy), E(Qx, Qy)
N = G.order()

print("p =", p, "(prime:", is_prime(p), ")")
print("curve: y^2 = x^3 + x,  #E =", E.order(), "= p+1")
print("G order N =", N, "=", factor(N))

residues, moduli = [], []
for q, e in factor(N):
    m = q**e
    kq = discrete_log((N//m)*Q, (N//m)*G, operation='+', ord=m)
    residues.append(kq); moduli.append(m)
    print(f"  k mod {m:>12} = {kq}")

k = CRT_list(residues, moduli)
print("\nk =", k)
print("verification: k*G == Q ->", k*G == Q)
