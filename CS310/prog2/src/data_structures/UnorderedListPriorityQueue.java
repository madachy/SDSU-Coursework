package data_structures;
import java.util.Iterator;
/**
 * William Fox cssc0917
 * Prog2, PriorityQueue, UnorderedListImplementation
 */
public class UnorderedListPriorityQueue<E extends Comparable<E>> implements PriorityQueue<E> {
    UnorderedList<E> list = new UnorderedList<E>();

    public boolean insert(E object) {
        list.addLast(object);
        return true;
    }
    public E remove() {
        return list.removeMin();
    }
    public E peek() {
        return list.findMin();
    }
    public boolean contains(E obj) {
        return list.contains(obj);
    }
    public int size() {
        return list.size();
    }
    public void clear() {
        list.clear();
    }
    public boolean isEmpty() {
        return list.isEmpty();
    }
    public boolean isFull() {
        return false;
    }
    public Iterator<E> iterator() {
        return list.iterator();
    }
}//Eof