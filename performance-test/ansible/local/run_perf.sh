ulimit -Sn 10000
#Argtest

../../scripts/perf_test.py x x x x x --only-header
for t in argtest
do
for m in 1 10 100
do
for n in 1 10 100
do
../../scripts/perf_test.py "ansible-playbook -M modules -i inventory${m}.yml playbook${n}.yml" ansible-playbook ${t} ${n} ${m} --no-header
done
done
done
