package data_structures;

import java.util.Comparator;
import java.util.ConcurrentModificationException;
import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * William Fox cssc0917
 * Prog2, PriorityQueue, UnorderedArrayImplementation
 */
public class UnorderedArrayPriorityQueue<E extends Comparable<E>> implements PriorityQueue<E> {
    private E[] array;
    private int size, capacity;
    private long modificationCounter;

    public UnorderedArrayPriorityQueue() {
        this(DEFAULT_MAX_CAPACITY);
    }

    public UnorderedArrayPriorityQueue(int capacity) {
        this.capacity = capacity;
        array = (E[]) new Comparable[capacity];
        modificationCounter = size = 0;
    }
    public boolean insert(E object) {
        if (isFull())
            return false;
        array[size++] = object;
        modificationCounter++;
        return true;
    }
    public E remove() {
        if (isEmpty())
            return null;
        int index = findHighestPriority();
        E temp = array[index];
        for (int i = index; i < size - 1; i++) { //Shifting Elements
            array[i] = array[i + 1];
        }
        size--;
        modificationCounter++;
        return temp;
    }
    public E peek() {
        if (isEmpty())
            return null;
        return array[findHighestPriority()];
    }
    public boolean contains(E obj) {
        for (int i = 0; i < size; i++)
            if (obj.compareTo(array[i]) == 0)
                return true;
        return false;
    }
    public int size() {
        return size;
    }

    public void clear() {
        modificationCounter++;
        size = 0;
    }
    public boolean isEmpty() {
        return size == 0;
    }
    public boolean isFull() {
        return size == capacity;
    }

    public Iterator<E> iterator() {
        return new IteratorHelper();
    }

    private class IteratorHelper implements Iterator<E> {
        private int iterIndex;
        private long stateCheck;

        public IteratorHelper() {
            stateCheck = modificationCounter;
            iterIndex = 0;
        }
        public boolean hasNext() {
            if (stateCheck != modificationCounter) throw new ConcurrentModificationException();
            return iterIndex < size;
        }
        public E next() {
            if (!hasNext())
                throw new NoSuchElementException();
            return array[iterIndex++];
        }
    }
    //My Helper Methods are below
    private int findHighestPriority() {
        E HighestPriority = array[0];
        int index = 0;
        for (int i = 1; i < size; i++)
            if (HighestPriority.compareTo(array[i]) > 0) {
                HighestPriority = array[i];
                index = i;
            }
        return index;
    }
}//Eof