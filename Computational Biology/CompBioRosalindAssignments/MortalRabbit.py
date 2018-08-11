def rabbits(months,dieLimit):
    live = [1,1]
    gen = 2
    while (gen < months):
        if (gen < dieLimit):
            live.append(live[gen-2] + live[gen-1])
        elif gen == dieLimit:
            live.append((live[gen-2] + live[gen-1]) - 1)
        else:
            live.append((live[gen-2] + live[gen-1]) - (live[gen-(dieLimit + 1)]))
        gen += 1
    print (live[-1])

rabbits(90,20)