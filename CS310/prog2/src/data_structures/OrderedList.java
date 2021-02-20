package data_structures;

import java.util.ConcurrentModificationException;
import java.util.Iterator;
import java.util.NoSuchElementException;

/**
/**
 * William Fox cssc0917
 * Prog2, Priority Queue OrderedList
 */
public class OrderedList<E extends Comparable<E>> implements Iterable<E> {
    private Node<E> head;
    private int size;
    private long modificationCounter;

    public OrderedList() {
        head = null;
        modificationCounter = size = 0;
    }
    public E removeMin() {
        if (isEmpty())
            return null;
        E temp = head.data;
        head = head.next;
        size--;
        modificationCounter++;
        return temp;
    }
    public E peek() {
        if (isEmpty())
            return null;
        return head.data;
    }
    public void insert(E obj) {
        Node<E> previous = null, current = head;
        Node<E> newNode = new Node<E>(obj);
        while (current != null && obj.compareTo(current.data) >= 0) {
            previous = current;
            current = current.next;
        }
        if (previous == null) { //Adding in first position
            newNode.next = head;
            head = newNode;
        } else {
            previous.next = newNode;
            newNode.next = current;
        }
        size++;
        modificationCounter++;
    }
    public boolean contains(E obj) {
        Node<E> pointer = head;
        while (pointer != null) {
            if (obj.compareTo(pointer.data) == 0) //Match
                return true;
            pointer = pointer.next;
        }
        return false;
    }
    public void clear() {
        head = null;
        modificationCounter++;
        size = 0;
    }
    public int size() {
        return size;
    }
    public boolean isEmpty() {
        return head == null;
    }
    public boolean isFull() {
        return false;
    }
    public Iterator<E> iterator() {
        return new IteratorHelper();
    }

    private class IteratorHelper implements Iterator<E> {
        private Node<E> tempNode;
        private long stateCheck;

        public IteratorHelper() {
            tempNode = head;
            stateCheck = modificationCounter;
        }
        public boolean hasNext() {
            if (stateCheck != modificationCounter) throw new ConcurrentModificationException();
            return (tempNode != null);
        }
        public E next() {
            if (!hasNext()) throw new NoSuchElementException();
            E temp = tempNode.data;
            tempNode = tempNode.next;
            return temp;
        }
        public void remove() {
            throw new UnsupportedOperationException();
        }
    }
    private class Node<E> {
        public E data;
        public Node<E> next;

        public Node(E obj) {
            data = obj;
            next = null;
        }
    }
}//Eof