package ch11;

import java.util.*;
public class PriorityQueueDemo {
    public static void printQ(Queue queue){
        while (queue.peek()!=null){
            System.out.println(queue.remove()+" ");
        }
        System.out.println();
    }
    public static void main(String[] args){
        PriorityQueue<Integer> priorityQueue = new PriorityQueue<Integer>();
        Random rand = new Random(47);
        for(int i=0; i<10; i++){
            priorityQueue.offer(rand.nextInt(i+10));
        }
        printQ(priorityQueue);

        List<Integer> ints = Arrays.asList(25,22,20,18,14,9,3,1,1,2,3,4,9,15,18,21,23,25);
        priorityQueue = new PriorityQueue<Integer>(ints);
        printQ(priorityQueue);

        priorityQueue = new PriorityQueue<Integer>(ints.size(), Collections.reverseOrder());
        priorityQueue.addAll(ints);
        printQ(priorityQueue);

        String fact = "EDUCATION SHOULD ESCHEW OBFUCATION";
        List<String> strings = Arrays.asList(fact.split(""));
        PriorityQueue<String> stringPQ = new PriorityQueue<String>(strings.size(), Collections.reverseOrder());
        stringPQ.addAll(strings);
        printQ(stringPQ);

        Set<Character> charSet = new HashSet<Character>();
        for (char c:fact.toCharArray())
            charSet.add(c);
        PriorityQueue<Character> charPQ = new PriorityQueue<Character>(charSet);
        printQ(charPQ);


    }
}
