# No Structure Required — POCTF 2026

Flag: POCTF{78.1406.5c12a4c7b6863f83.LOG2OEI5IDDSRXXTH6QO27V3YW}

Giriş endpoint'i JSON gövdesini doğrudan document store sorgusuna geçiriyordu. username ve password alanlarına {"$ne":null} vererek j.abernathy olarak giriş yaptım. Browse sayfasındaki col parametresi herhangi bir koleksiyonu açıyordu; secrets koleksiyonunda takım flag'i duruyordu.

![terminal](terminal.png)
